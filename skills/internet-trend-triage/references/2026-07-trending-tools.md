# 2026-07 Trending Tools — Session Evidence
Retrieved: 2026-07-15
Purpose: support priority-ranked triage for daily external-source scans.

## Sources
- `awesome-llm-apps` — https://github.com/shubhamsaboo/awesome-llm-apps
- `openinterpreter/openinterpreter` — https://github.com/openinterpreter/openinterpreter
- `vshulcz/deja-vu` — https://github.com/vshulcz/deja-vu
- Coasty — https://coasty.ai/docs
- HN frontpage — https://news.ycombinator.com/
- GitHub Trending — https://github.com/trending

## Executable notes
- `deja` installed to `/home/hatem/.local/bin/deja`; version 0.6.0; warmup builds local index.
- `awesome-llm-apps` cloned to `/home/hatem/Documents/awesome-llm-apps/`.
- `deja sources` shows: Claude 2 sessions, OpenCode 0, Codex 0. On this host sqlite3 CLI was unavailable for opencode indexing.
- Reddit is blocked by robots.txt for generic fetches; treat as manual-only unless a dedicated Reddit auth path is active.
- Open Interpreter install failed in `/tmp/oi-env` because Python 3.14 is newer than PyO3 0.20.3 and `tiktoken` wheel build aborted. Suspension marker: revisit with Python 3.12 or a prebuilt `tiktoken` build path for 3.14.

## Tool-use notes
- `x_search` can fail with `personal-team-blocked:spending-limit` after repeated Grok calls. Do not retry the same query on x_search; switch to GitHub/HN fetcher paths.
- Reddit blocks generic autonomous fetchers. Do not fetch `reddit.com` directly from general fetch paths; use a dedicated skill or manual pass only.

## Priority rankings from this session
Immediate action:
- `awesome-llm-apps`
- `deja-vu`
Evaluate soon:
- `openinterpreter/openinterpreter`
- Coasty API
Watchlist:
- GitHub trending repos from the July 15, 2026 fetch: OpenCut, destructive_command_guard, telegram-serverless, Vibe-Trading.
