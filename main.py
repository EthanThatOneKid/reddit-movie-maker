# py main.py "subreddit" "javascript"
# py main.py "post" "b53fvi"
# helpers\post_renderer\application.windows64\post_renderer "Title" "Ethan" "Hello world" "C:/Users/acer/Documents/GitHub/reddit-movie-maker/helpers/post_renderer/1.png"
# processing-java sketch=pwd`/post_renderer --run

import os, sys, json, requests, subprocess

# Helpers
def create_post_cmd(title, user, body):
    file_path = os.path.dirname(os.path.realpath(__file__))
    temp_path = "{}/posts/{}.png".format(file_path, 0)
    cmd_template = "{} --sketch={} --run \"{}\" \"u/{}\" \"{}\" \"{}\""
    cmd = cmd_template.format(env["processing-java"], env["sketch"], title, user, body, temp_path)
    return cmd

def get_subreddit_posts(r):
    print(r)
    posts = []
    for child in r["data"]["children"]:
        gimme_data = child["data"]
        if len(gimme_data["selftext"]) == 0: continue
        posts.append([
            gimme_data["title"],   # title
            gimme_data["author"],  # user
            gimme_data["selftext"] # body
        ])
    return posts

def get_post_comments(r):
    posts = []
    title = r[0]["data"]["children"][0]["data"]["title"]
    for child in r[1]["data"]["children"]:
        if child["kind"] != "t1": continue
        gimme_data = child["data"]
        if len(gimme_data["body"]) == 0: continue
        posts.append([
            title,                # title
            gimme_data["author"], # user
            gimme_data["body"]    # body
        ])
    return posts

def create_reddit_url():
    config = sys.argv[1]
    id = sys.argv[2]
    endpoints = json.load(open('./data/endpoints.json'))
    endpoint = endpoints[config]
    url = endpoint["head"] + id + endpoint["foot"]
    return url

# Main Process
env = json.load(open("./helpers/dotenv.json"))

#url = create_reddit_url()
reddit = json.load(open('./recent_test2.json'))
for post in get_post_comments(reddit)[:10]:
    cmd = create_post_cmd(post[0], post[1], post[2])
    subprocess.call(cmd)
#reddit = requests.get(url).json()
#posts = get_subreddit_posts(reddit)
#open('recent_test2.json', 'w').write(json.dumps(reddit, indent=2))

#post = make_post("title", "u/EthanThatOneKid", "body blah blah blah body")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# now child exec pls
# open('recent_test.json', 'w').write(json.dumps(reddit, indent=2))
