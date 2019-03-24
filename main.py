# py main.py "subreddit" "javascript"
# helpers\post_renderer\application.windows64\post_renderer "Title" "Ethan" "Hello world" "C:/Users/acer/Documents/GitHub/reddit-movie-maker/helpers/post_renderer/1.png"
# processing-java sketch=pwd`/post_renderer --run

import os, sys, json, requests

# Helpers
def make_post(title, user, body):
    file_path = os.path.dirname(os.path.realpath(__file__))
    temp_path = "{}/{}.png".format(file_path, 0)
    cmd_template = "{} --sketch={} --run \"{}\" \"{}\" \"{}\" \"{}\""
    cmd = cmd_template.format(env["processing-java"], env["sketch"], title, user, body, temp_path)
    return cmd

def create_reddit_url():
    config = sys.argv[1]
    id = sys.argv[2]
    endpoints = json.load(open('./data/endpoints.json'))
    endpoint = endpoints[config]
    url = endpoint["head"] + id + endpoint["foot"]
    return url

# Main Process
env = json.load(open("./helpers/dotenv.json"))

url = create_reddit_url()
reddit = requests.get(url).json()

post = make_post("title", "u/EthanThatOneKid", "body blah blah blah body")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# now child exec pls
# open('recent_test.json', 'w').write(json.dumps(reddit, indent=2))
