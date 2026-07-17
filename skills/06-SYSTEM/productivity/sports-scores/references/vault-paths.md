# Sports Data Vault Paths
# Sports Data Vault Paths

## Canonical locations
### Hatem's second brain
- `/home/hatem/Documents/Hatem Nad/World Cup 2026.md` -- main tournament tracker
- `/home/hatem/Documents/Hatem Nad/WorldCup-Archive/` -- archived World Cup snapshots
- `/home/hatem/Documents/Hatem Nad/pages/[world-cup-2026.md` -- quick Obsidian reference note
- `/home/hatem/Documents/Hatem Nad/logseq/bak/Archived-YYYY-MM-DD/` -- retired Logseq backups

### Hafsa's vault
- `/home/hatem/Documents/Hafsa/📅 اليوميات/YYYY-MM-DD.md` -- daily summary note (Cairo times)

## Preferred score sources

| Source | URL | Notes |
|--------|-----|-------|
| Wikipedia | `en.wikipedia.org/wiki/2026_FIFA_World_Cup` | Best for group-stage structure. Use browser_console JS extraction. |
| 365scores | `365scores.com/football/2026-fifa-world-cup/` | Reliable fallback; use browser_console full-text extraction if the page is large. |
| ESPN | `espn.com/soccer/scoreboard` | Recent results only; subpages often 404. |
| FIFA official | `fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/matches` | Often empty or blocked. |
| FilGoal / Yalla Kora / Flashscore | -- | Unreliable from outside the Middle East / blocked by Cloudflare. Avoid. |

## Known issues
- `web_search` and `web_extract` often fail without `FIRECRAWL_API_KEY`. Default to browser extraction.
- Google CAPTCHA blocks automated searches. Go to Wikipedia directly.
- Patch/edit loops: if `patch` keeps finding duplicate matches in tables, use a small terminal-backed Python replacement over repeated patch retries.
- Update the active tracker file directly; archive old content under `WorldCup-Archive/` instead of deleting.
- Patch/edit loops in edit-heavy files: if patch keeps finding repeated matches for the same block, prefer a small terminal-backed Python replacement over repeated patch retries.
