# World Cup 2026 — bracket extraction notes

## Problem
Group-stage pages list results nicely, but Round of 32 and later use merged roster/bracket tables in Wikipedia. Date cells often say "June 29 – City", while opponent cells may show placeholder winners ("Winner Match 74") until the match is played.

## Verified source as of 2026-06-29
- Main article: `https://en.wikipedia.org/wiki/2026_FIFA_World_Cup`
- Dedicated subpage: `https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_round_of_32`
- Knockout bracket table usually sits above the `## Round_of_32` heading and uses merged cells with `rowspan`.

## Extraction tip
Instead of parsing the full bracket, grep the raw HTML for stable anchors:
- Locate the "Round of 32" section by `id="Round_of_32"`.
- From the bracket table rows, extract lines containing `June 29` and adjacent team cells.
- In many edits, the round-of-32 row contains:
  - `June 29 – <City>` in a merged date cell
  - `<a href="/wiki/Germany...">Germany</a>` followed later by `<a href=".../Germany_vs_Paraguay"...">Round of 32</a> vs Germany (June 29)` in the Paraguay row.
- Cross-check both sides; if one side shows "Winner Match XX", it's still future/tbd.

## Quick June 29 Round of 32 reference (from Wikipedia)
- Germany vs USA — Foxborough — 19:00 Cairo
- Netherlands vs Senegal — Guadalupe — 19:00 Cairo
- Brazil vs Ivory Coast — Houston — 22:00 Cairo
- Spain vs Austria — Monterrey — 01:00 Cairo (next day)

## Pitfalls
- File may say dates that disagree with the live schedule. Trust Wikipedia bracket over cached vault data on dates.
- Group schedule tables and knockout tables are separate HTML tables; don't assume one regex covers both.
- FIFA.com returns bot-block text; avoid as source.
