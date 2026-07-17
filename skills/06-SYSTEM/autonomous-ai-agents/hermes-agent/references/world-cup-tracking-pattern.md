# World Cup Tracking Pattern

How to keep a sports tournament tracker updated in an Obsidian vault using web
search + file editing.

## When to Use

- User is following a sports tournament (World Cup, Champions League, etc.)
- User wants match results, group standings, and schedules updated
- User has a dedicated vault file for the tournament

## Architecture

```
YouTube/Web Search → Extract Results → Update Tracker File → Update Templates
```

## Workflow

### 1. Search for Latest Results
Use web search or YouTube to find the latest match results:
- Search: "World Cup 2026 results [date]"
- YouTube: Official channels (FIFA, CBS Sports, etc.)
- Use `yt-dlp --write-auto-sub` for video transcripts

### 2. Update the Main Tracker File
The main file contains all historical data, group standings, and upcoming matches.
Update sections:
- Match results table (append new rows)
- Group standings (recalculate points, goal difference)
- Statistics (goals per game, top scorers)
- Upcoming matches schedule

### 3. Update Daily Templates
For each match day, update the daily template with:
- Match results
- Key moments
- Player of the day
- Updated group standings

### 4. Update Top Scorers
Maintain a running list of top scorers across the tournament.

## File Structure

```
vault/
├── [Tournament].md          # Main tracker (all data)
├── Templates/
│   ├── [tournament]-tracker.md  # Updated copy with latest data
│   └── [tournament]-daily.md    # Daily match template
└── pages/
    └── [tournament].md      # Logseq page (if using Logseq)
```

## User-Specific Setup

- User uses Logseq for the Hatem Nad vault
- User has a `World Cup 2026.md` file with full tournament data
- User wants results updated after each match day
- User prefers Arabic labels with English team names

## Pitfalls

### Logseq Sync
Logseq uses markdown files but may have its own indexing. After editing `.md` files,
Logseq should auto-detect changes. If not, trigger a re-index.

### YouTube Block
YouTube may block automated access. Use `yt-dlp` with impersonation or fall back
to web search if videos are unavailable.

### Rate Limits
Don't search for every match individually. Batch searches by match day.

### Data Accuracy
Always cross-reference at least 2 sources for match results. Official FIFA site is
primary source.

### Template Drift
When updating the tracker, also update the daily template to reflect the latest
standings. The template should always show "after today" state.

## Example Update Flow

```bash
# 1. Search for results
web_search("World Cup 2026 results June 22")

# 2. Parse results
# 3. Update World Cup 2026.md
patch("World Cup 2026.md", old_match_row, new_match_row)

# 4. Update group standings
patch("World Cup 2026.md", old_standings, new_standings)

# 5. Update daily template
write_file("Templates/worldcup-2026-daily.md", updated_daily_content)
```

## Priority Order

1. Match results (most important — factual)
2. Group standings (derived from results)
3. Schedule (future matches)
4. Statistics (nice to have)
5. Personal notes (user's opinions, predictions)

---

*World Cup Tracking Pattern — حفصة 🇲🇦💋*
