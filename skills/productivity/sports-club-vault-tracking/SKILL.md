---
name: sports-club-vault-tracking
description: MUST USE when building or operating a vault-based sports club tracking system — Egyptian football (Al-Ahly, Zamalek, etc.) or any club where the user wants match logs, schedules, standings, squad, injuries, H2H, progression, coach stats, season progress, and news curated in an Obsidian vault. Covers vault scaffold, official-source selection, Templater template, Dataview dashboard setup, Bases view, per-match update routine, Index sync cron, and canonical vault routing.
---

# Sports Club Vault Tracking

Build and maintain a markdown vault that tracks a football club across all competitions.

## When to use

- User asks to "follow a club in my vault" / "organize team news and results"
- Building vault structure for Egyptian Premier League, CAF, domestic cups
- Updating match results after user provides scores

## Vault scaffold

Create this exact folder tree under the user's vault root. For Al-Ahly, use canonical path inside the primary vault, e.g. `/home/hatem/Documents/Hafsa/01-Projects/Al-Ahly/`.

```
<ClubVault>/
├── Overview.md                 # landing page + Dataview dashboard
├── Dashboard.md                # full dashboard: last match, top scorer, ratings, injuries, H2H, progression, coach stats
├── Progress.md                 # season progress bar, points target, form
├── Bases-View.md               # optional Bases view for tabular/kanban-like browsing
├── Squad.md                    # players + coach + season ratings + yellow cards
├── Injuries.md                 # injuries, suspensions, absence notes
├── H2H.md                      # head-to-head history vs selected opponent
├── Progression.md              # league position progression by round
├── Coach.md                    # coach stats: W/D/L, win rate, goals for/against, best XI
├── Matches/
│   ├── Log.md                  # chronological match results
│   ├── Schedule.md             # upcoming matches with time/venue
│   └── Template-Match.md       # Templater template for new match note
├── Competitions/
│   ├── Premier-League.md       # league standings + club matches
│   ├── CAF-Champions-League.md # CAF matches + progress
│   └── Cup.md                  # domestic cup + super cup
└── News/
    └── Clips.md                # official links, videos, reactions
```

### Naming convention
- Match notes: `YYYY-MM-DD - <competition> vs <opponent>.md`
- Keep Arabic-only labels in user-facing tables.

### Frontmatter properties
Use these fields in match/squad files for Dataview queries:
- `date`, `competition`, `opponent`, `result`, `status` (`played|upcoming|cancelled`)
- `venue`, `referee`, `time`, `stadium`
- Squad: `name`, `number`, `position`, `season_rating`, `season_goals`, `season_assists`, `yellow_cards`, `injury_status`, `notes`

## File templates

See `templates/al-ahly-scaffold.zip` for drop-in copies of every file above.

## Primary sources

### High-trust (prefer first)
- **Club official site** — e.g. `alahlyegypt.com/ar` for Al-Ahly. Browser automation works reliably here; avoid fetch MCP.
- **Wikipedia** — full season tables, match logs, squad.

### Watch-list sites (access unreliable)

Egyptian aggregate sites commonly block `fetch` MCP and may 404 under browser automation due to aggressive anti-bot routing. See `references/egypt-football-sources.md` for the current source-access bank.

Rule of thumb:
- If `fetch` returns 404 / `Page failed to be simplified` → don't retry the same URL.
- Try Wikipedia as fallback.
- Ask the user to paste the result if live scraping fails.

### Social/community
- Facebook groups can provide crowd reactions but require login; store as `source` links only, never attempt fetch.

## Update workflow

### After every match (user-supplied result)
1. Ask for: date, opponent, score, competition, goal scorers, venue.
2. Update `Matches/Log.md` — append a new row.
3. Update `Competitions/<league>.md` standings table if league position changed.
4. Update `Overview.md` "أخر نتيجة" block.
5. Update `Matches/Schedule.md` — mark completed, shift next match to "أخر نتيجة" if needed.

Update order matters: user-facing files first (Overview, Log), source-of-truth files second (Competition tables).

### Standings update pattern
- On manual update: user confirms current table OR agent scrapes reliable source.
- Never guess standings; if source is unavailable, mark `(قيد التحديث)` and note the failed source.

## Automation
- Cron: create a profile-local cron to sync Overview/Dashboard/Index after match updates. Example prompt: refresh Dataview sections in Overview.md and update Index.md; do not delete old matches; output only changed paths.
- Templater: store template under `.obsidian/templates/Al-Ahly-Match.md` and reference it from the skill.

## User conventions observed

- Egyptian fan context: "الأهلي", "دوري المصري", "كأس مصر", "دوري أبطال أفريقيا" are fixed labels — keep Arabic.
- Date format: `DD/MM` for fixtures, `YYYY-MM-DD` for archive note.
- Time zone: all times Cairo (GMT+3).
- Vault path: canonical path is inside the primary vault, e.g. `/home/hatem/Documents/Hafsa/01-Projects/Al-Ahly/`. Move old duplicates to `/Archive/` rather than deleting.

## Pitfalls

- **fetch-blocked sports sites**: filgoal/yallakora/goal.com Egypt subdomains routinely return 404 to MCP fetch; do not spend multiple turns retrying identical fetch calls.
- **Facebook groups**: cannot be read without login; only add as link source.
- **Goal .com Egypt slug drift**: `/eg/` Arabic paths often 404; use `.com` international Egypt selector only if needed.
- **Mixing languages**: vault must stay Arabic-only for user-facing tables and labels.
