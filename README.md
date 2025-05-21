# X to Bluesky Reposter Bot

This bot reposts everything a user posts on X (Twitter) to Bluesky.

Test Accounts:

[@XtoBluesky](https://x.com/XtoBluesky) on X

[@autoreposter.bsky.social](https://bsky.app/profile/autoreposter.bsky.social) on Bluesky

## Setup
1. Clone the repo.
2. Create a `.env` file based on `.env.example`.
3. Fill in your Twitter handle, Bearer Token, and Bluesky handle & password.

**Note:** Tweets will be posted as Bluesky posts under your Bluesky account.

## Local Run
```bash
pip install -r requirements.txt
python main.py
