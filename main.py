# py main.py "subreddit" "javascript"
# helpers\post_renderer\application.windows64\post_renderer "Title" "Ethan" "Hello world" "C:/Users/acer/Documents/GitHub/reddit-movie-maker/helpers/post_renderer/1.png"
# processing-java sketch=pwd`/post_renderer --run

import sys, json, requests

def create_reddit_url():
    config = sys.argv[1]
    id = sys.argv[2]
    endpoints = json.load(open('./data/endpoints.json'))
    endpoint = endpoints[config]
    url = endpoint["head"] + id + endpoint["foot"]
    return url

url = create_reddit_url()
print(url)
reddit = requests.get(url).json()

open('recent_test.json', 'w').write(json.dumps(reddit, indent=2))
