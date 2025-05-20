import os
import json
import requests
from atproto import Client

STATE_FILE = 'seen_ids.json'

def load_seen():
    """Load the set of seen tweet IDs from STATE_FILE (or return empty set)."""
    try:
        return set(json.load(open(STATE_FILE)))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen(seen):
    """Save the set of seen tweet IDs back to STATE_FILE."""
    with open(STATE_FILE, 'w') as f:
        json.dump(list(seen), f)

def fetch_tweets():
    """
    Fetch the most recent tweets for TWITTER_HANDLE.
    Returns a list of dicts: [{'id': ..., 'text': ...}, ...].
    If we hit a rate limit (429), returns an empty list.
    """
    BEARER = os.environ['TWITTER_BEARER_TOKEN']
    handle = os.environ['TWITTER_HANDLE']
    headers = {"Authorization": f"Bearer {BEARER}"}

    # 1) Look up the numeric user ID for the handle
    resp = requests.get(
        f"https://api.twitter.com/2/users/by/username/{handle}",
        headers=headers
    )
    resp.raise_for_status()
    user_id = resp.json()['data']['id']

    # 2) Fetch recent tweets (no retweets, no replies)
    params = {
        "exclude": "retweets,replies",
        "max_results": 5,
        "tweet.fields": "created_at"
    }
    resp = requests.get(
        f"https://api.twitter.com/2/users/{user_id}/tweets",
        headers=headers,
        params=params
    )
    if resp.status_code == 429:
        print("⚠️  Hit Twitter rate limit, skipping this run.")
        return []
    resp.raise_for_status()

    data = resp.json().get('data', [])
    print(f"Fetched {len(data)} tweets from @{handle}")
    return [{'id': t['id'], 'text': t['text']} for t in data]

def post_to_bluesky(text: str):
    """Authenticate to Bluesky and create a new post with the given text."""
    bsky = Client()
    bsky.login(os.environ['BLUESKY_HANDLE'], os.environ['BLUESKY_PASSWORD'])
    bsky.post(text=text)
    print("✅ Posted to Bluesky:", text[:50])

def main():
    seen = load_seen()
    tweets = fetch_tweets()

    for tw in tweets:
        if tw['id'] in seen:
            continue
        print("→ Reposting tweet:", tw['text'])
        post_to_bluesky(tw['text'])
        seen.add(tw['id'])

    save_seen(seen)

if __name__ == '__main__':
    main()