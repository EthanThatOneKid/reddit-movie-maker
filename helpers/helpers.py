import sys, json

def create_reddit_url():
    endpoints = json.load(open('./data/endpoints.json'))
    config = sys.argv[1]
    id = sys.argv[2]
    url = endpoints[config]["head"] + id + endpoints[config]["foot"]
    return url
