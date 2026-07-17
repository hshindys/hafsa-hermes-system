# World Cup Data Source Troubleshooting

## Verified sources (June 2026)

### Wikipedia Parse API — RELIABLE
- Endpoint: `https://en.wikipedia.org/w/api.php?action=parse&page=<PAGE>&prop=text&format=json`
- Works for: match lists, round pages, group pages, team pages
- Returns rendered HTML inside `parse.text.*` or `parse.text`
- Strip tags with regex or parse JSON carefully
- Example pages:
  - `2026_FIFA_World_Cup`
  - `2026_FIFA_World_Cup_round_of_32`
  - `2026_FIFA_World_Cup_group_<LETTER>`

### FIFA.com — NOT USABLE VIA CURL
- React/JS app; curl returns shell with scripts only
- Match data requires browser/JS execution
- Do not attempt HTML parsing of fifa.com via curl

### 365soccer.com — BLOCKED
- Root URL redirects to `/lander` instantly
- Cannot extract match data via curl as of June 2026

## Fallback sources
- Hacker News Algolia API for news discussion
- Official match report PDFs referenced in Wikipedia citations (hosted on fdp.fifa.org)
- Team pages on Wikipedia for historical context

## Known match data points (verified June 2026)
- Egypt vs Australia: Round of 32, Match 88, July 3 2026, 21:00 Cairo, AT&T Stadium Arlington
- Egypt topped Group G; Australia advanced as runner-up