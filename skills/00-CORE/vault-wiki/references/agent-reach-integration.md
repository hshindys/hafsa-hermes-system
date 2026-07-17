# Agent Reach Integration Notes

## Install Layout (this machine)
- venv: `~/.agent-reach-venv`
- skill copy: `~/.hermes/profiles/hafsa/skills/agent-reach/`
- prefer running via venv binary: `source ~/.agent-reach-venv/bin/activate && agent-reach ...`

## Verified Commands
- Health check: `agent-reach doctor --json`
- Quick watch: `agent-reach watch`
- Setup/install docs: `agent-reach install --env=auto`

## Active Channels
- GitHub: gh CLI
- Twitter/X: OpenCLI
- Reddit: OpenCLI
- YouTube: yt-dlp
- Bilibili: bili-cli
- RSS/Atom: feedparser
- Exa search: mcporter Exa free tier
- Web pages: Jina Reader (`https://r.jina.ai/URL`)

## Channel Caveats
- LinkedIn: MCP not configured; needs `linkedin-scraper-mcp` + mcporter config
- Xueqiu: blocked without browser login cookie; use `agent-reach configure --from-browser chrome`

## Usage Rule
- Use agent-reach for web/social retrieval; do not hand-roll curl for platforms it already covers.
- For World Cup briefs, prefer Wikipedia API + optional Exa search, not blocked score sites.