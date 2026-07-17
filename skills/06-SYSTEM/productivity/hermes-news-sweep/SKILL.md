---
name: hermes-news-sweep
description: "Build and operate a scheduled news-sweep system with Hermes: cron-driven web fetching, HTML parsing, HackerNews fallback, and vault archive. Use when the user asks for news automation, Hermes Oracle, topic monitoring, daily briefings, or scheduled web-to-vault harvesting."
tags:
  - cron
  - automation
  - news
  - web
  - vault
  - fallback
---

# Hermes News Sweep

## Trigger
Use when the user asks for:
- News automation / Hermes Oracle-style monitoring
- Daily briefings or topic sweeps
- Scheduled collection of latest headlines into the vault
- Fallback from blocked search APIs to live sources

## Core approach
1. Place a single Python script under `~/.hermes/scripts/`
2. Run it via `cronjob` with `no_agent=true` so the script output is delivered
3. Archive Markdown output into `/home/hatem/Documents/Hafsa-1/AI-News-Sweep/`

## Verified stack
- `requests`
- `beautifulsoup4` + `lxml`
- Optional: `html5lib`
- HackerNews Algolia API for fallback data
- Python interpreter from `~/.hermes/hermes-agent/venv/bin/python3`

## Script contract
The script must:
- Write one Markdown file per topic into the configured `BASE_DIR`
- Include a generated-at timestamp and a simple Markdown table
- Print a small JSON summary to stdout: `{"ok": true, "topics": {"AI": {"count": N, "path": "..."}, ...}}`
- Fail loud on missing deps; do not swallow errors silently

## Cron job pattern
- Path: script must live under `~/.hermes/scripts/`
- Use absolute path for `script`: `hafsa_news_sweep.py`
- Time zone: `Africa/Cairo` for all schedules
- Recommended: `0 5 * * *` for morning briefings

## Fallback order
1. HTML scraping from reliable news sites
2. If topic count is low, append HackerNews Algolia results for that topic
3. Report sources clearly so the user can adjust URLs later

## Sources to rotate
- TechCrunch AI category
- The Verge AI section
- ESPN / FIFA for sports topics
- HackerNews `hn.algolia.com` queries for fallback

## Pitfalls
- `x_search` may be blocked by provider spend limits; do not depend solely on it
- Some sports URLs 404 after seasons start; prefer FIFA/ESPN stable paths
- Cron runner cannot run `pip install`; install deps into the venv first

## User preferences
- Be concise, direct, active execution
- No numbered lists; tables preferred for scans
- Prefer Moroccan Darija with Arabic as the working cadence when initiated in Arabic
- Embed fixes into skills, not just memory