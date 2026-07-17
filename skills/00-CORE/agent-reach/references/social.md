# Social Media & Communities

Xiaohongshu, Twitter/X, Bilibili, V2EX, Reddit.

## Xiaohongshu / XiaoHongShu (multi-backend)

Xiaohongshu has three backends. **Run `agent-reach doctor --json` first to see the xiaohongshu `active_backend`**, then use the corresponding command group.

### Backend A: OpenCLI (desktop-first, reuses browser login)

```bash
# Search notes
opencli xiaohongshu search "query" -f yaml

# Read note text + engagement data (use full URL from search results, including xsec_token)
opencli xiaohongshu note "NOTE_URL" -f yaml

# Comments (nested comments supported)
opencli xiaohongshu comments NOTE_ID -f yaml

# Home feed
opencli xiaohongshu feed -f yaml

# Public user profile notes
opencli xiaohongshu user USER_ID -f yaml
```

> Requires Chrome with OpenCLI extension. If `AUTH_REQUIRED` appears, the user is not logged into Xiaohongshu in Chrome.

### Backend B: xiaohongshu-mcp (server scenarios)

```bash
# If not logged in: check status, then show QR code
mcporter call 'xiaohongshu.check_login_status()' --timeout 120000
mcporter call 'xiaohongshu.get_login_qrcode()' --timeout 120000

# Search
mcporter call 'xiaohongshu.search_feeds(keyword: "query")' --timeout 120000

# Note detail + comments (feed_id and xsec_token from search results)
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "...", xsec_token: "...")' --timeout 120000
```

> First call downloads ~150MB headless browser automatically; always pass `--timeout 120000`. If not logged in, `search` will hang; run `check_login_status` first.

### Backend C: xhs-cli (legacy fallback; upstream stopped updates in March 2026)

```bash
xhs search "query"          # search
xhs read NOTE_ID_OR_URL     # read note
xhs comments NOTE_ID_OR_URL # comments
xhs hot                     # hot posts
xhs feed                    # recommended feed
```

> Known instability: `xhs user` / `xhs user-posts` / `xhs favorites` may return API errors. New setups should prefer backend A/B.

### General notes

> **xsec_token requirement**: Xiaohongshu enforces xsec_token — never read a note with a bare note_id. Flow: `search/feed` -> full URL/ID -> read. Same for all 3 backends.
>
> **Rate limits**: High-frequency requests trigger CAPTCHA. Pause 2–3 seconds between operations.
>
> **Write actions (post/comment/like)**: Read-only is recommended. `xhs-cli v0.6.x` write actions may return 406 due to signature issues.

## Twitter/X (twitter-cli)

### Stable commands

```bash
# Home timeline (most stable)
twitter feed -n 20

# Read tweet + replies
twitter tweet URL_OR_ID

# Read long posts / X Articles
twitter article URL_OR_ID

# User timeline
twitter user-posts @username -n 20

# User profile
twitter user @username
```

### Potentially unstable commands

```bash
# Search tweets (Twitter changes GraphQL often, may 404)
twitter search "query" -n 10

# likes (since 2024: only self, platform-limited)
twitter likes
```

### search failure retry chain (stop on success)

1. Retry once directly (transient failures are common): `twitter search "query" -n 10`
2. Upgrade then retry: `pipx upgrade twitter-cli && twitter search "query" -n 10`
3. Switch to OpenCLI fallback (desktop, reuses browser login): `opencli twitter search "query" -f yaml`
4. Otherwise use stable commands like `twitter feed` / `twitter user-posts @somebody`

### Important notes

> **Install**: `pipx install twitter-cli` (use v0.8.5+)
>
> **Auth**: Recommended via Cookie-Editor export: `TWITTER_AUTH_TOKEN` + `TWITTER_CT0`. Automatic extraction is unavailable in SSH/Docker/headless environments.
>
> **IP risk**: Do not call from VPS/datacenter IPs at high frequency, especially for followers/following. Use residential proxy or local machine.
>
> **OpenCLI fallback**: On desktop with OpenCLI installed: `opencli twitter search/article/user-posts -f yaml` works via browser session; no cookie env vars needed.
>
> **Output format**: Use `--yaml` or `--json` for structured output friendly to AI agents.

## Bilibili

> ⚠️ **Do not use yt-dlp for Bilibili** (412 blocks are comprehensive and unavoidable). Use `bili-cli` / OpenCLI instead.

```bash
# Search / hot / video details (bili-cli, read-only, no login required)
bili search "query" --type video -n 5
bili hot -n 10
bili video BVxxx

# Subtitles (OpenCLI, requires desktop Chrome)
opencli bilibili subtitle BVxxx
```

> For advanced usage (audio transcription, direct API fallback), see [references/video.md](video.md).

## V2EX (public API)

No auth required.

### Hot topics

```bash
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
```

### Node topics

```bash
# node_name examples: python, tech, jobs, qna, programmers
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"
```

### Topic detail

```bash
# topic_id from URL, e.g. https://www.v2ex.com/t/1234567
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
```

### Topic replies

```bash
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

### Member info

```bash
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

### Python example

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# Hot topics
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} replies)")

# Node topics
node_topics = ch.get_node_topics("python", limit=5)

# Topic detail + replies
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])

# Member info
user = ch.get_user("Livid")
```

> **Nodes list**: https://www.v2ex.com/planes

## Reddit (multi-backend, login required)

**Reddit has no zero-config path**: anonymous `.json` endpoints are blocked (403), and official API applications have been rarely approved since November 2025. Both backends depend on login state. Run `agent-reach doctor --json` to check `reddit.active_backend`. Mainland China access requires a proxy.

### Backend A: OpenCLI (desktop-first, reuses browser login)

```bash
# Search posts
opencli reddit search "query" -f yaml

# Read post + comments
opencli reddit read POST_ID -f yaml

# Browse subreddit / hot / popular
opencli reddit subreddit LocalLLaMA -f yaml
opencli reddit hot -f yaml
opencli reddit popular -f yaml

# Subreddit metadata (subscribers, description)
opencli reddit subreddit-info LocalLLaMA -f yaml
```

> Requires Chrome with reddit.com login.

### Backend B: rdt-cli (legacy/server fallback; upstream stopped updates in March 2026)

```bash
rdt search "query" --limit 10
rdt read POST_ID
rdt sub python --limit 20
rdt popular --limit 10
rdt all --limit 10
```

> **Install**: `pipx install 'git+https://github.com/public-clis/rdt-cli.git'` (PyPI is outdated; use v0.4.2+ from GitHub). Run `rdt login` before searching/reading; on headless servers, manually set cookies as shown by `doctor`.
>
> Prefer `--yaml` output for AI agents.

### Advanced option: official API + PRAW (existing credential holders only)

Users who registered a Reddit script app before November 2025 (`client_id`/`client_secret`) may use PRAW against the official API with 100 QPM free tier. New applications require human approval and personal projects are routinely declined. **Do not recommend this path to new users.**
