# Football / World Cup Data Sources

Lessons from trying to fetch Egypt vs Australia 2026 WC data.

## Wikipedia

### Which pages exist
- Group pages like `2026_FIFA_World_Cup_Group_C` exist for completed groups
- Country pages like `Egypt_at_the_2026_FIFA_World_Cup` may not exist yet for future/unplayed matches
- Direct country-page curl can return empty content or redirect

### Use API, not raw HTML
`curl -s "https://en.wikipedia.org/w/api.php?action=parse&page=PAGE_NAME&prop=text&format=json"`

The parse API returns a stable HTML-ish payload that `grep` and Python regex can filter reliably.

## 365soccer.com
- **Blocks curl**: returns HTTP 200 with `<script>window.location.href="/lander"</script>` — it's an anti-bot redirect.
- **Do not use with vanilla curl**; finds no useful data and wastes time.
- Worth trying with a real browser / headless browser only.

## Fallback strategy for match data
1. Wikipedia API parse endpoint (first choice)
2. FIFA official match centre (if URL known)
3. BBC Sport / The Guardian match reports (human-readable)
4. For real-time odds/scores, use authenticated sports APIs or official league endpoints

## 2026 Egypt vs Australia clue
- Date user gave: **3 July 2026**
- Match likely exists on Wikipedia once it's played or in pre-tournament previews
- If page doesn't exist yet, check knockout-stage pages after group phase ends
