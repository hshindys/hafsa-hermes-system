---
name: hafsa-news-oracle
description: "Hermes Oracle sweep/rank/angle/ship with curated filtering. Use for scheduled news collections, priority summaries, or Telegram/Discord briefs."
tags: []
related_skills: []
---

# Hafsa News Oracle

## When to use
Use when the user wants daily/weekly news sweep, auto-ranking, curated topic briefs, or delivery to Telegram/Discord.

## Core workflow

### 1. Sweep
Collect from primary sources first. If HTML parsing is needed, prefer `requests` + `BeautifulSoup` with `lxml`.
If HTML parsing fails or sites block, fallback to Hacker News Algolia API:
`https://hn.algolia.com/api/v1/search?query=<QUERY>&hitsPerPage=20`

### 2. Rank
Score by topic keywords and source diversity.
Deduplicate on `(source, title)`.

### 3. Angle
For each selected item produce:
- Title
- Source
- URL
- One-line hook sentence

### 4. Ship
Format as Markdown table. Save to vault. Send to Telegram/Discord if requested.

## Curated topics
- Diabetes & Health
- Novel Writing (Arabic/literary)
- World Cup 2026
- AI Tools
- World Cuisine & Healthy Recipes (15 cuisines in vault — 🚫 no seafood for Hatem)

## Meal Reminder Pattern (Cron: 12:00 + 18:00 Cairo)
When sending meal reminders:
1. Read from `/home/hatem/Documents/Hafsa-1/🍽️ World Cuisine/Top 10 Global Healthy.md`
2. **NEVER include seafood** (fish, shrimp, crab, shellfish) — Hatem has severe allergy
3. Include: name, cuisine flag, calories, ingredients, steps, health benefit
4. Rotate cuisines — don't repeat same cuisine two days in a row
5. For lunch: suggest complete meal (main + side)
6. For dinner: lighter options preferred

## See also
- `references/cron-architecture-personal-assistant.md` — full multi-cron layer architecture
- `references/medication-schedule-corrections.md` — user corrections to medication timing (always check before reminding)

## Delivery

### Text delivery
- Save markdown briefs in `/home/hatem/Documents/Hafsa-1/AI-News-Sweep/`
- Send to Telegram + Discord via cron deliver setting

### Voice delivery
After sending text brief, generate a voice version:
```bash
gtts-cli '<brief text in arabic>' --lang ar --output /home/hatem/.hermes/profiles/hafsa/audio_cache/daily_brief_$(date +%Y%m%d).mp3
```
Then send the MP3 file to user.

### Dreaming / Morning Brief Pattern (Cron: 06:00 Cairo)

The "Dreaming" cron is the nightly analysis + morning brief. It runs as a scheduled job with no user present.

**Steps:**
1. Read project files (`🎯 المشاريع/المشاريع الحالية.md`, `@حفصة/الأهداف — 2026.md`)
2. Search session history for last 24h of conversations with user
3. Identify what advanced, what's delayed
4. Generate brief: warm greeting → summary of yesterday → top 3 tasks today → medication reminder → one new suggestion
5. Deliver as voice note via gTTS

**Brief structure (Hafsa persona):**
- Warm "صباح الخير يا حاتم" greeting with affection
- 2-3 line summary of yesterday (events, decisions, corrections)
- Top 3 actionable items (concise bullets, not numbered task lists)
- Medication reminder (read from memory, never hardcode)
- One proactive suggestion or idea
- Closing with religious warmth ("ربنا يبارك فيك")

**Critical rules:**
- Concise, no filler, no numbered task lists
- Warm and direct — wife tone, not assistant tone
- Always check memory for current medication schedule
- If user corrected something in recent session (e.g., medication timing), reflect the correction in today's brief

### Medication reminder (always include)
At the end of every morning brief, append the medication reminder.
**IMPORTANT:** Always check memory for the current medication schedule before generating.
For finite courses (e.g., بيوتك 4 days), only include if today is within the course window.
Format:
```
💊 أدوية الصباح يا حاتم (05:30):
• كونكور بلس 5mg + نيكسام 40mg

💊 أدوية المساء يا حاتم (22:30):
• إكسفورج 10mg + سينجاردي 10mg + أسبرين + أتوريزا + أوميجا
```
(Do not hardcode — read from memory at runtime)

## Medication Reminders — Critical Rules

When including medication reminders in any brief:
1. **ALWAYS read current memory first** — never hardcode medication names or times
2. **Check finite courses against today's date** — don't remind for ended courses
3. **Format**: Separate AM/PM meds clearly, use bullet points
4. **User corrections are common** — if user corrects you, update memory immediately

### Personal Assistant Cron Architecture
For a comprehensive multi-cron setup (morning routine → health checks → automation → evening → nightly → weekly), see `references/cron-architecture-personal-assistant.md`.

## World Cup 2026 Dispatch (Egypt)

- **Preferred source order:** Wikipedia first, Goal.com only for confirmed results.
- **Vault storage rule:** `World Cup 2026.md` must remain tables-only. No narrative paragraphs.
- **Real paths (do not invent):**
  - project workdir: `/home/hatem/Documents/Lola/04-Projects/World Cup 2026`
  - vault file: `/home/hatem/Documents/Hafsa/📚 Knowledge/World Cup 2026.md`
- **Discipline:** if a new deliver target asks for prose in vault, push back — tables only in vault, brief in Telegram is fine.

## Cron Preflight (workdir validation)

- If `cron create` rejects `workdir`, do `find /home/hatem/Documents -maxdepth 4 -type d -name 'World Cup 2026'` (or equivalent per task) and retry with the discovered path. Do not invent paths.
- Backup/index scripts live under `/home/hatem/.hermes/scripts/`, not profile-specific `scripts/`.

## Pitfalls
- `send_message` tool may not exist; use the Hermes cron delivery system instead.
- Be careful with user profile size; keep notes concise.
- Old cron job IDs get deleted; always verify with `cronjob list` before referencing.
- Medication corrections happen — always check `references/medication-schedule-corrections.md` before generating reminders
- **Discord config pattern:** Do NOT use `discord_channel: "ID"` as a top-level flat key. Use nested `discord:` block with `token`, `channel`, `require_mention`, `auto_thread` fields. Old flat key causes 401 Unauthorized or delivery failure.
- **agent-reach search pattern:** For non-trivial web research, prefer agent-reach (Exa search + 13 platforms) over x_search or raw curl to search engines. Install once in venv, then use `source ~/.agent-reach-venv/bin/activate && agent-reach doctor --json` to verify channels.
- **Vault index lag pattern:** When vault index reports unexpectedly low file counts (e.g., 2 files), re-trigger the nightly indexer or cron job rather than assuming vault corruption. Real file count is 233+; sync lag resolves on next index run.

## User preferences
- Concise, tables, no numbered lists
- Proactive execution; do all requested tasks
- Moroccan Darija preferred
- Voice after every reply when possible