# py main.py "subreddit" "javascript"

import sys, json, requests

def create_reddit_url():
    endpoints = json.load(open('./data/endpoints.json'))
    config = sys.argv[1]
    id = sys.argv[2]
    url = endpoints[config]["head"] + id + endpoints[config]["foot"]
    return url

url = create_reddit_url()
print(url)
reddit = requests.get(url).json()

open('recent_test.json', 'w').write(json.dumps(reddit, indent=2))
