# Egypt Football Source Access Bank

Last updated: 2026-07-08

## Verified access patterns

### alahlyegypt.com/ar
- Status: **works reliably in browser automation**
- Use: club news, transfers, coach names, official announcements
- Slug example: `/ar` homepage, no special auth required

### ar.wikipedia.org/wiki/الدوري_المصري_الممتاز_للأقدام_<season>
- Status: **works reliably via fetch and browser**
- Use: full season tables, match results, squad lists
- Requires: exact season URL suffix (e.g. `2025–2026`)

### kooora.com
- Status: **frontpage loads in browser; league/standings URLs return 404**
- Use: headlines / hub only
- Pitfall: `/?league=1&season=2026` → 404
- Fallback: Wikipedia if standings needed

### filgoal.com
- Status: **404 on league pages**
- Use: does not provide data under current bot detection
- Fallback: `alahlyegypt.com/ar` + Wikipedia

### goal.com (Arabic)
- Status: **404 on Egypt league standings**
- Use: does not provide Egypt standings under current slug
- Fallback: international Arabic selector not reliable for Egypt league table

### yallakora.com
- Status: **404/500 on league pages**
- Use: not accessible for structured data
- Fallback: `alahlyegypt.com/ar` + Wikipedia

### 365scores.com
- Status: **fetch returns "Page failed to be simplified from HTML"**
- Use: not automatable via MCP fetch
- Fallback: browser may load, but structure not confirmed for Egypt EPL

## Source priority for Al-Ahly vault

1. `alahlyegypt.com/ar` — browser fetch + direct snapshot
2. `ar.wikipedia.org` — fetch + browser
3. Facebook group — link-only source, no scrape
4. `yallakora.com`, `filgoal.com`, `goal.com/eg`, `365scores.com` — keep as notes but do not rely for automated pulls

## Retry policy

- One fetch attempt per source.
- If it fails once → mark source as blocked for this session.
- Fallback chain: club official site → Wikipedia → ask user to paste text.

## Notes

- Goal.com browser dropdown contains "Egypt (العربية)" but page routing is unreliable; do not depend on it during automation.
- Facebook groups need login; never assign as primary.
