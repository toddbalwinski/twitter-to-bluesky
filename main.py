import os
import time
import json
from atproto import Client
import requests
from dotenv import load_dotenv

load_dotenv()
twitter_bearer = os.getenv("TWITTER_BEARER_TOKEN")
twitter_handle = os.getenv("TWITTER_HANDLE")
bluesky_handle = os.getenv("BLUESKY_HANDLE")
bluesky_password = os.getenv("BLUESKY_PASSWORD")

SEEN_FILE = "seen_posts.json"

# Load IDs of posts already reposted to Bluesky
def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

# Fetch latest posts from the user timeline
# Uses Twitter API v2 Bearer Token for app-only auth
def fetch_posts():
    url = f"https://api.twitter.com/2/users/by/username/{twitter_handle}"
    headers = {"Authorization": f"Bearer {twitter_bearer}"}
    # Get user ID
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    user_id = resp.json()["data"]["id"]

    # Fetch X posts
    timeline_url = f"https://api.twitter.com/2/users/{user_id}/tweets?exclude=replies,retweets&tweet.fields=created_at"
    resp = requests.get(timeline_url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("data", [])

# Post text to Bluesky
def post_to_bluesky(text):
    client = Client()
    client.login(bluesky_handle, bluesky_password)
    client.post(text)
    return True


def main():
    seen = load_seen()
    while True:
        tweets = fetch_posts()
        for tw in tweets:
            tid = tw["id"]
            if tid in seen:
                continue
            text = tw["text"]
            try:
                post_to_bluesky(text)
                print(f"Reposted to Bluesky: {text[:30]}...")
                seen.add(tid)
            except Exception as e:
                print("Error posting to Bluesky:", e)
        save_seen(seen)
        time.sleep(60)

if __name__ == "__main__":
    main()