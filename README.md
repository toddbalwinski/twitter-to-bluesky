# Twitter to Bluesky Repost Bot

Automatically mirror tweets from an Twitter (X) account into your Bluesky feed.

**Example Accoutnts**
- Twitter Account: [@XtoBluesky](https://x.com/XtoBluesky)
- Bluesky Account: [@autoreposter.bsky.social](https://bsky.app/profile/autoreposter.bsky.social)

---

## Project Overview

This lightweight Python bot will:

1. **Fetch** the latest tweets (excluding retweets/replies) from a specified X account via the Twitter API v2  
2. **Repost** each new tweet as a Bluesky post using the official AT Protocol client  
3. **Track** which tweets have already been reposted in a simple JSON file  
4. **Automate** execution on a cron schedule with GitHub Actions (free tier)

---

## Tech Stack & Tools

- **Language & Runtime**  
  - Python 3.8+
- **Core Libraries**  
  - [`atproto`](https://pypi.org/project/atproto/) — Bluesky AT-Protocol client  
  - [`requests`](https://pypi.org/project/requests/) — HTTP client for Twitter API v2  
- **External APIs**  
  - **Twitter API v2** (OAuth 2 Bearer Token) — fetch user timeline  
  - **Bluesky AT Protocol** — post content to Bluesky  
- **State Persistence**  
  - `seen_ids.json` — local JSON file storing reposted tweet IDs  
- **CI/CD & Scheduling**  
  - **GitHub Actions** — runs `main.py` every 5 minutes (or on manual dispatch)  
  - **Git & GitHub** — source control, secret storage, workflow orchestration  

---
## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/X-to-Bluesky-Repost-Bot.git
cd X-to-Bluesky-Repost-Bot
```

### 2. Create a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize your state file

Create an empty JSON array so the bot can track reposted tweets:

```bash
echo '[]' > seen_ids.json
```

---

## Configuration

The bot reads credentials and settings from environment variables.

| Variable                  | Description                                           |
|---------------------------|-------------------------------------------------------|
| `TWITTER_HANDLE`          | The X username to mirror (e.g. `my_handle`)           |
| `TWITTER_BEARER_TOKEN`    | Your Twitter v2 API Bearer token                      |
| `BLUESKY_HANDLE`          | Your Bluesky handle (e.g. `you.bsky.social`)          |
| `BLUESKY_PASSWORD`        | Your Bluesky account password                         |

#### Locally

```bash
export TWITTER_HANDLE="your_handle"
export TWITTER_BEARER_TOKEN="AAAAAAAA...your_token"
export BLUESKY_HANDLE="you.bsky.social"
export BLUESKY_PASSWORD="your_password"
```

#### In GitHub Actions

1. Go to **Settings → Secrets and variables → Actions** in your repo  
2. Add each of the four variables above as **new repository secrets**

---

## Run Locally

With your env-vars set and virtualenv activated:

```bash
python main.py
```

You should see console output like:

```
Fetched 2 tweets from @your_handle
→ Reposting tweet: Hello Bluesky! #x2bskytest
✅ Posted to Bluesky: Hello Bluesky! #x2bskytest
```

`seen_ids.json` will be updated automatically.

---

## Deployment via GitHub Actions

We use a simple workflow (`.github/workflows/repost.yml`) that:

- Checks out your code  
- Installs Python & dependencies  
- Runs `main.py`  
- Commits any updates to `seen_ids.json` (even if empty) back to the repo  

### Key points

- **Schedule**: runs every 5 minutes (`cron: '*/5 * * * *'`)  
- **Manual dispatch**: you can also click **Run workflow** in the Actions tab  
- **Permissions**: ensure “Read and write repository contents” is enabled under **Settings → Actions → General**  

_No external servers or credit cards required — everything runs on GitHub’s free tier._

---

## How It Works

1. **Lookup user ID** via `GET /2/users/by/username/:username`  
2. **Fetch recent tweets** via `GET /2/users/:id/tweets?exclude=retweets,replies&max_results=5`  
3. **Handle rate-limits** (429) gracefully by skipping the run  
4. **Login & post** to Bluesky with `bsky = Client(); bsky.login(...); bsky.post(text)`  
5. **Persist state** in `seen_ids.json` and push back to GitHub  

---

## File Structure

```
├── main.py                      # core bot logic
├── requirements.txt             # Python deps: atproto, requests
├── seen_ids.json                # state file (start as [])
└── .github/
    └── workflows/
        └── repost.yml           # GitHub Actions workflow
```

---

## Obtaining Your API Credentials

### Twitter API v2

1. Sign up for a free Developer account at https://developer.x.com/  
2. Create a new App within a Project  
3. Copy your **Bearer Token** from the “Keys and tokens” page  

### Bluesky

1. Sign up for a free account at https://bsky.app/  
2. Use your handle & password directly with the `atproto` client  

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---
