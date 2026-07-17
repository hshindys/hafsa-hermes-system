# Hermes Agent Update & Version Info

## Current Version (2026-06-22)
- **v0.17.0** (2026.6.19) — "The Reach Release"
- Already installed on this system

## How to Update
```bash
# Method 1: CLI (requires user confirmation)
hermes update

# Method 2: Git pull + reinstall (works without confirmation)
cd ~/.hermes/hermes-agent && git pull && pip install -e . --quiet
```

## v0.17.0 Key Features
- **iMessage Plugin** — send/receive iMessage via Photon (no Mac needed)
- **Raft Platform Adapter** — connect to Raft agent network
- **Desktop App v2** — RTL, notifications, subagent streaming, VS Code terminal
- **Background Subagents** — agents run in background
- **Image Editing** — generation + editing
- **Memory Tool Upgrade** — major improvement to memory system
- **Skills Hub Browser** — rehauled
- **Dashboard Profile Builder** — full profile + secure login

## Release Stats
- ~1,475 commits · ~800 merged PRs · 1,693 files changed
- 300+ issues closed · 245 community contributors

## Note
`hermes update` command requires interactive confirmation. Use `git pull && pip install -e .` for non-interactive updates.
