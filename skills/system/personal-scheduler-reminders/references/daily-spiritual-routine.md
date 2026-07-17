# Daily Spiritual Routine — unified scheduler

## Goal
Generate one consistent daily spiritual schedule — prayer times, Quran block, adhkar, Asma Al Husna, writing block, family call, sleep dhikr — and inject it into today’s daily note.

## Canonical implementation

### Config file
`~/.hermes/config/routine.toml`

Key fields:
- `location.city/country/latitude/longitude/timezone`
- `location.calculation_method = 5` for Egypt/Cairo
- `vault.path` = canonical vault containing daily notes
- `vault.daily_note_pattern` = e.g. `Daily/{date}.md`
- `vault.section_header` = section to upsert
- `schedule.*_minutes_after_*` = offsets for each block
- `cache.dir` = local prayer-time cache

### Script
`/home/hatem/Documents/Hafsa/daily_routine.py`
Also deployed to:
`~/.hermes/profiles/hafsa/scripts/daily_routine.py`

Responsibilities:
1. Load `routine.toml`.
2. Fetch Cairo prayer times from Aladhan v1; cache daily JSON under `~/.hermes/cache/`.
3. Build timed rows for:
   - Fajr + wake-up adhkar
   - Quran block
   - Morning adhkar
   - Asma Al Husna of the day
   - Dhuhr/Asr
   - Writing block
   - Maghrib + evening adhkar
   - Family call
   - Isha + sleep adhkar
   - Sleep
4. Render a compact RTL markdown table.
5. Upsert into today’s daily note under the configured section header.
6. Skip rewrite if the section already exists.

### Cron job
Create a script-only cron that runs at **03:15 Cairo**:

- `schedule: 15 3 * * *`
- `script: daily_routine.py`
- `no_agent: true`
- `deliver: local`
- `workdir: /home/hatem/Documents/Hafsa`

## Adhkar content
Use concise authentic texts from `أذكار-حصن-المسلم.md`:
- wake-up
- morning
- evening
- sleep

## Migration / cleanup rules
When replacing an older per-slot adhkar system:
1. Add the unified script/cron first.
2. Verify one manual run succeeds.
3. Remove the old agent-mode adhkar scheduler cron.
4. Remove expired one-shot adhkar crons.
5. Keep only prayer-time reminder crons if they are still needed.

## Pitfalls
- `cronjob` rejects absolute script paths. Use a relative filename that resolves under `~/.hermes/scripts/`.
- `tomllib` requires Python 3.11+; if missing, install `tomli`.
- Aladhan timing strings may include suffixes like ` (EEST)`; truncate to first 5 chars (`HH:MM`).
- Do not store adhkar texts inline in cron prompts; keep them in a markdown file or the Python script.
- Do not run this in parallel with another job that edits the same daily-note section without serialization.
