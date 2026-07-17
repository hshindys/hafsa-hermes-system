# Al-Ahly Dashboard Setup Reference

## Source hierarchy
1. Primary: https://www.alahlyegypt.com/ar
2. Secondary: Wikipedia season/competition pages
3. Tertiary: https://www.kooora.com, https://www.yallakora.com
4. Community: Facebook group links only, no automated fetch

## Dashboard layout
- Overview.md: compact landing with 1-line quick links + Dataview tables for last 5 results + next 3 matches
- Dashboard.md: full dashboard with last match, man of the match, standings, top scorer, last-match ratings, season ratings, injuries/H2H/progression/coach stats
- Progress.md: season progress bar, points target, win/draw/loss split, goal difference
- Bases-View.md: optional Bases view pulling from Matches/Squad/Progress

## Templater template
Path: `.obsidian/templates/Al-Ahly-Match.md`
Key fields:
- date, competition, opponent, result, status
- venue, referee, time, stadium
- man_of_the_match, attendance, weather
- season_progress, coach
- scorers table, notes, highlights link

## Frontmatter conventions
- Matches: date, competition, opponent, result, status, venue, referee, time, stadium
- Squad: name, number, position, season_rating, season_goals, season_assists, yellow_cards, injury_status, notes
- Competitions: season, competition, status
- Use `status: played|upcoming|cancelled`

## Notes
- Arabic-only labels in user-facing tables and headings.
- Cairo timezone everywhere.
- Never auto-retry blocked sports sites; fall back to Wikipedia or user-supplied data.
