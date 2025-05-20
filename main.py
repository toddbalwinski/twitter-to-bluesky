import os, json
from atproto import Client
import requests

# load state
try:
    seen = set(json.load(open('seen_ids.json')))
except:
    seen = set()

# Bluesky login
bsky = Client()
bsky.login(os.environ['BLUESKY_HANDLE'], os.environ['BLUESKY_PASSWORD'])

# fetch X tweets (replace with your fetch logic)
def fetch_tweets():
    url = f"https://api.twitter.com/2/timelines/by/username/{os.environ['TWITTER_HANDLE']}"
    # …use your Bearer token, parse tweet text & ids…
    # return list of {'id':id, 'text':text}
    return []

# post back to Bluesky
def post_to_bsky(text):
    bsky.post(text)

tweets = fetch_tweets()
for tw in tweets:
    if tw['id'] in seen:
        continue
    post_to_bsky(tw['text'])
    seen.add(tw['id'])

# save state
with open('seen_ids.json','w') as f:
    json.dump(list(seen), f)
