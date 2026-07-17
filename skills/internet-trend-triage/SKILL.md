---
name: internet-trend-triage
description: >
  MUST USE when the user asks "what's new", “شوف ايه الجديد على YouTube/Reddit/GitHub/HN/GitLab”, wants a ranked brief of today’s AI/agent/automation trends,
  or asks to scan external sources and produce a priority-organized summary.
  Covers GitHub Trending, HN, Substack/blogs, technical docs, release pages, and structured daily briefs.
  Enforces fallback discipline when search tools are throttled or blocked.
  NOT for: posting/commenting/liking; Reddit automation when robots/auth is blocked.
license: MIT
metadata:
  author: hafsa
  version: "0.1"
---

# Internet Trend Triage

Use this when the user wants a curated, priority-ranked brief of new tools, repos, news, or techniques from the internet.

## Core output shape
- Group by priority: Immediate action / Evaluate soon / Watchlist
- For each item: source, one-line value, why it matters to the user’s stack, and a concrete next action
- Keep it short, scannable, and actionable

## Discovery ladder (preferred order)
1. Direct fetched pages/docs for known repositories or products
2. HN frontpage + GitHub Trending
3. Substack/blog roots for release announcements or deep dives
4. Search fallbacks only when the above are insufficient

## Failure rules
- If Grok/x_search is throttled or out of credits, do not retry. Switch to ladder order above.
- If Reddit is blocked or unauthenticated, skip it and tell the user why; do not keep retrying.
- If fetcher content is truncated, fetch a narrower page or a README/docs path instead.
- Do not invent rankings. If a result is incomplete, mark it "incomplete".

## Session evidence
See `references/2026-07-trending-tools.md` for the July 2026 fetched results and install paths.
That file is reusable scaffolding: update it when new requests come in.

## Privacy/scope
- Prefer public pages with no login walls.
- Never bypass robots.txt explicitly; if blocked, note it and move on.
- Avoid paywalled sources; if unavoidable, treat them as "walled" and continue with public alternatives.
