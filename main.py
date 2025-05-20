import os, json, requests
from atproto import Client

STATE_FILE = "seen_ids.json"

def load_seen():
    try:
        return set(json.load(open(STATE_FILE)))
    except FileNotFoundError:
        return set()

def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)

def fetch_tweets():
    """Return a list of dicts: [{'id':id, 'text':text}, …]"""
    BEARER = os.environ["TWITTER_BEARER_TOKEN"]
    handle = os.environ["TWITTER_HANDLE"]
    headers = {"Authorization": f"Bearer {BEARER}"}

    # 1) look up the user ID
    r = requests.get(f"https://api.twitter.com/2/users/by/username/{handle}", headers=headers)
    r.raise_for_status()
    user_id = r.json()["data"]["id"]

    # 2) fetch their recent tweets (no retweets, no replies)
    params = {
        "exclude": "retweets,replies",
        "max_results": 5,                # adjust as needed
        "tweet.fields": "created_at"
    }
    r = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets",
                     headers=headers, params=params)
    r.raise_for_status()
    data = r.json().get("data", [])
    # debug print
    print(f"Fetched {len(data)} tweets from @{handle}")
    return [{"id": t["id"], "text": t["text"]} for t in data]

def post_to_bluesky(text):
    bsky = Client()
    bsky.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_PASSWORD"])
    # this is the atproto call to create a new post
    bsky.post(text=text)

def main():
    seen = load_seen()
    tweets = fetch_tweets()
    for tw in tweets:
        if tw["id"] in seen:
            continue
        print("→ reposting:", tw["text"][:50])
        post_to_bluesky(tw["text"])
        seen.add(tw["id"])
    save_seen(seen)

if __name__ == "__main__":
    main()
