---
name: medication-reminders
description: MUST USE when setting up medication reminders, drug schedules, pill reminders, or cron-based medication notifications.
---

# Medication Reminders

Build and manage cron-based medication reminder systems with accurate date/time awareness.

## Core Principles

### NEVER Guess Time or Date

- **Always run `terminal('date "+%Y-%m-%d %A %H:%M %Z"')` first** before answering any time-sensitive medication question
- Never declare "today is day N of medication" without verifying the actual date
- If the user says "yesterday" or "today", verify against system clock — users may be tired, confused, or in a different timezone context
- When user corrects your date calculation, accept it gracefully and update — do not argue or recalculate without checking

### Verify Before Stating

- When user asks "is it time for X medication?" — check system time first
- When user says "today is day N of medication" — verify the start date and current date
- When setting up reminders, confirm the current date to calculate remaining course days

## Cron-Based Reminder Architecture

### Standard Touchpoints

For a typical AM+PM medication schedule:

| Job | Schedule | Purpose |
|-----|----------|---------|
| Date/Time briefing | 05:00 daily | Day name + Gregorian + Hijri + current time |
| AM meds reminder | 05:30 daily | Morning medications |
| Specific dose reminder | 10:30 daily | Mid-day doses (e.g. antibiotics) — only during course window |
| PM meds reminder | 22:30 daily | Evening medications |

### Building Cron Jobs

- `schedule`: cron expression in user's timezone (default Africa/Cairo UTC+3)
- `deliver`: 'telegram' for Telegram delivery
- `prompt`: Self-contained, includes date verification step
- `repeat`: 'forever' for daily, or omit for one-shot

### Limited-Course Medications

For medications with a fixed duration (e.g., 4-day antibiotic course):

1. Record start date in memory (and this reference file)
2. Calculate end date (start + duration - 1)
3. **Confirm with user:** "Started on [date], ends on [date]. Is that correct?" — do NOT skip this step
4. Set up reminder cron with date-checking logic in prompt
5. After course ends, the cron's conditional logic silences it; tell user it's done

Example prompt for course-limited meds:

```
Check today's date. If it's between [start] and [end]:
- If 2 days or less remaining: send reminder with "فاضل يومين" warning
- If last day: send "آخر جرعة النهارده ✅"
- If course finished: reply SILENTLY
If outside this range, reply SILENTLY.
```

## Date Formatting for Arabic Users

- Include Arabic day name (الأحد، الاثنين، الثلاثاء، etc.)
- Include both Gregorian and Hijri dates when possible
- Use 12-hour format with صباح/مساء indicators
- Example format: `25 يونيو 2026 — الخميس — 05:30 فجراً`

## Current Schedule

Update active medications from `references/hatem-current-meds.md`.

## Pitfalls

### 1. Off-by-One on Course Days

User said "started yesterday" but you calculated from today. Always confirm with the user rather than asserting.

**Real example:** User said "البيوتك بدأ امبارح" (biotic started yesterday). Agent calculated "day 3" but it was day 2. The user corrected it.

**Rule:** When user says "started yesterday", compute: if today is the Nth, yesterday was N-1. So the course spans [N-1, N+duration-2]. VERIFY by asking "Is today day 1, 2, or 3?" before committing to a day count.

### 2. Timezone Confusion

User's timezone is Africa/Cairo (UTC+3). Verify server timezone matches expectations with `date` command.

### 3. Memory Full

Medication entries can overflow memory limits. Keep them compact: use abbreviations, update existing entries rather than adding new ones. Remove stale or less important entries to make room when near limit.

### 4. Duplicate Reminders

When user corrects a medication time, update the existing cron job rather than creating a new one. Use `cronjob(action='list')` first to find the job_id.

### 5. Forgetting to Verify

The most common mistake: stating "today is day 3" without checking. The user WILL correct the agent. Always run `date` first.

### 6. Multi-Round Correction Pattern

When the user gives a medication schedule, expect 2-4 correction rounds:
- Round 1: Wrong time (e.g., "نيكسام باليل مش الصبح")
- Round 2: Wrong dose timing (e.g., "البيوتك مرتين في اليوم")
- Round 3: Wrong course duration (e.g., "4 أيام بس")
- Round 4: Date calculation errors (see Pitfall 1)

**Strategy:** After the first correction, re-read the ENTIRE schedule back to the user in a clean table before creating crons. Confirm each drug's time AND duration. Only create crons after explicit user confirmation ("تمام" or "صح").

### 8. Post-Update Cron Recovery

After gateway restarts, config changes, or system updates:
- List all crons and look for `"state": "paused"` on jobs that should be active
- Resume them explicitly with `cronjob(action='resume', job_id=...)`
- Medication and prayer crons commonly get paused after profile updates — verify before assuming they're running

**Real example (2026-06-25):** Agent listed "سينجاردي 10mg" in the morning (10:30) slot. User corrected: "خليه مساء" (make it evening). The agent started explaining pharmacology ("لو النص يقلب بالليل...") instead of just accepting the correction.

**Rules:**
- When the user says "ده مساء مش صباح" or "ده بالليل", IMMEDIATELY move that drug to the PM slot. Do NOT explain why the original timing might have been acceptable.
- The user knows their body and their doctor's instructions. Your job is to record, not to medical-judge.
- Pattern: "سينجاردي → PM", "بيوتك → AM", "إكسفورج → PM", "أسبرين بروتكت → PM"
- After correcting timing, read back the FULL updated schedule in a table for confirmation.

## Cron Script Path Pitfall

**Symptoms:** Medication cron fails with:
```
python: can't open file '/home/hatem/Documents/.../scripts/create-daily-note.py': [Errno 2]
```

Or bash medication scripts return "No such file or directory" even though the job should have a working script.

**Root cause:** Cron `script` paths resolve under `~/.hermes/profiles/<profile>/scripts/`. If the actual script lives at `~/.hermes/scripts/`, the cron can't find it.

**Fix:**
```bash
# Copy shared scripts into the profile scripts directory
cp ~/.hermes/scripts/reminder-morning-meds.sh ~/.hermes/profiles/<profile>/scripts/
cp ~/.hermes/scripts/reminder-evening-meds.sh ~/.hermes/profiles/<profile>/scripts/
chmod +x ~/.hermes/profiles/<profile>/scripts/reminder-*.sh
```

**Prevention:** When creating notification scripts, place them under BOTH locations:
- `~/.hermes/scripts/` for global availability
- `~/.hermes/profiles/<profile>/scripts/` for cron resolution

**Verification:**
```bash
# Test directly
bash ~/.hermes/profiles/<profile>/scripts/reminder-morning-meds.sh
# Then verify cron last_status == "ok" with `cronjob(action='list')`
```

## Reminder Message Template

```
💊 تذكير الأدوية — [time period]

[قائمة الأدوية]

📅 [date info if relevant]
⏰ الساعة دلوقتي: [current time]
```

Keep it warm but brief. User needs facts, not paragraphs.

## Related Cron Patterns (from real session)

This session also created companion non-medication reminders:

| Cron | Schedule | Purpose |
|------|----------|---------|
| Date/Time briefing | 05:00 daily | Arabic day + Gregorian + Hijri + time |
| Health Check | 10:00 Tue/Fri | Weekly health check-in (BP, glucose, mood, pain) |
| Resolver | 21:00 daily | Priority list from session history |
| Daily Summary | 21:00 daily | Personal summary of the day (conversations, decisions) |
| Grill Me | 13:00 Sat/Thu | Deep question to understand user better |
| Loop (nightly) | 02:00 daily | Auto-process pending tasks overnight |
| Follow-up Auto | 17:00 workdays | Remind user about pending follow-ups |
| Skill-ification | 14:00 Saturday | Weekly review of workflows to save as skills |

When setting up medication reminders, be aware of these companion crons so they don't conflict in timing or overwhelm the user.
