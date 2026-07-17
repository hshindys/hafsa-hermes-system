---
name: personal-scheduler-reminders
description: >
  Personal scheduling, medication reminders, and date/time awareness system.
  MUST USE when setting up any cron-based reminder, daily schedule, medication tracker,
  or when the user asks about current date/time in Arabic/Hijri/Gregorian.
  Covers: medication schedules with finite courses, cron job creation for life reminders,
  date/time formatting with Arabic day names + Hijri dates, and proactive daily briefings.
---

# Personal Scheduler & Reminders

## When to use

- Setting up medication reminder cron jobs
- Creating personal daily/weekly reminders (not news — see `hafsa-news-oracle` for that)
- User asks about current date, day of week, or time
- Tracking a finite course of medication (e.g., 4-day antibiotic course)
- Any cron-based reminder that delivers to Telegram/Discord/WhatsApp

## Core Capabilities

### Date & Time Awareness

Always check the real system date before answering time-sensitive questions:

```bash
date '+%Y-%m-%d %A %H:%M'  # Gregorian + English day name + time
```

Calculate Hijri using installed `hijri-converter`:

```bash
python3 -c "from hijri_converter import convert; g = convert.Gregorian.today(); print(f'{g.year}-{g.month}-{g.day} => {g.to_hijri()}')"
```

Never guess dates. The agent must always know:
- **Current Gregorian date** (ميلادي)
- **Current Hijri date** (هجري)
- **Day of week in Arabic** (الأحد، الإثنين، الثلاثاء، الأربعاء، الخميس، الجمعة، السبت)
- **Current time in user's timezone** (default: Africa/Cairo UTC+3)

**Self-check rule:** whenever the user corrects the date, weekday, or Hijri, treat it as a hard signal that the agent should have checked proactively, then re-verify via terminal before responding further.

Format dates for user:
> 📅 **25 يونيو 2026 — الخميس**
> 🕔 **الساعة 05:30 فجراً بتوقيت القاهرة**

If formatter dependency is missing:
```bash
pip install hijri-converter
# or
pip install hijridate
```

### 1. Medication Schedule Management

When user provides a medication schedule:

1. **Parse the schedule** — extract drug names, doses, times, frequency, duration
2. **Create cron jobs** for each medication time slot
3. **Track finite courses** — note start date and end date
4. **Handle conditional reminders** — only remind during the course window

**Key pattern:** Check the current date inside each cron job. If the course has ended, reply silently (no message sent). This avoids spamming reminders after the course is done.

#### Medication cron job template:
```
Schedule: "30 5 * * *" (daily at 05:30)
Prompt: Check if today is within [start_date, end_date]. If yes, send reminder
for [drug_name] [dose]. If no, reply SILENTLY.
```

#### Formatting medication reminders:
- Use 💊 emoji before drug names
- Group by time slot (morning/evening)
- Include dosage in mg
- Note which drugs are time-sensitive vs. optional
- Add end-date warnings: "فاضل يومين في الكورس"

### 3. General Life Reminders

For non-medication reminders (exercise, appointments, meals, prayers):
- Create one cron job per reminder
- Use specific schedules (daily, weekly, or one-shot ISO timestamp)
- Keep messages brief and warm
- Include context (e.g., "وقت صلاة الفجر يا حاتم 🕌")

#### Islamic Prayer Reminders

For each of the 5 daily prayers, create a separate cron job with Arabic Egyptian warm reminders. Prayer times are dynamic; never static-schedule reminders that drift.

> **Default workflow:** For adhkar after Fajr/Asr, use the "Adaptive Prayer-Time Reminders" pattern. Only use fixed-time daily crons for non-prayer general reminders.

| Prayer | Anchor | Tone |
|--------|--------|------|
| Fajr, Dhuhr, Asr, Maghrib, Isha | actual Cairo times from API | 2-3 lines, authentic dua/salawat, warm Egyptian dialect |

Message style:
- 2-3 lines max
- Include one short Quranic dua or salawat
- Use warm Egyptian dialect ya habibi/ya sando
- Islamic reminders must be authentic, not generic — use real duas

#### Adaptive Prayer-Time Reminders (Real Cairo Times)

For adhkar/prayer reminders that must follow actual daily prayer times rather than fixed clock times:

1. **Create an agent-mode scheduler cron** that runs daily at 03:15 Cairo. It must:
   - Hit `api.aladhan.com/v1/timingsByCity` for Cairo
   - Pin today's timings in memory
   - Create one-shot exact-time reminder jobs for adhkar slots
2. **Adhkar reminder slots:** Fajr+15 min and Asr+15 min. Use `no_agent=True` + exact-text shell scripts.
3. **Script path requirement:** scripts MUST live under `~/.hermes/scripts/` with `.sh`/`.bash` extension. Profile-local paths are silently rejected.
4. **Audit cron:** run every 2 days to backfill any missing one-shot crons for the audit window.

#### One-shot creation pattern

Inside the agent-mode scheduler cron, for each adhkar slot:

```python
import datetime, requests
q = requests.get("https://api.aladhan.com/v1/timingsByCity", params={"city":"Cairo","country":"Egypt","method":"5"}, timeout=15)
timings = q.json()["data"]["timings"]
for slot, label in [("Fajr","morning-adhkar"), ("Asr","evening-adhkar")]:
    t = datetime.datetime.strptime(timings[slot], "%H:%M") + datetime.timedelta(minutes=15)
    iso = t.strftime("%Y-%m-%dT%H:%M:00+03:00")
    # create one-shot cron: schedule=iso, no_agent=True, script='<name>.sh'
```

#### Adhkar script templates

`~/.hermes/scripts/adhkar-morning.sh`:
```bash
#!/bin/bash
echo "📿 أذكار الصباح
اللهم بك أمسينا وبك أصبحنا وبك نعيش وبك نموت وإليك النشور.

---
من حصن المسلم — يقال بعد صلاة الفجر"
```

`~/.hermes/scripts/adhkar-evening.sh`:
```bash
#!/bin/bash
echo "🌇 أذكار المساء
اللهم بك أمسينا وبك أصبحنا.

---
من حصن المسلم — يقال بعد صلاة العصر"
```

Read full adhkar texts from `Religion/أذكار الصباح.md` and `Religion/أذكار المساء.md`.

#### Pitfalls

1. **Script jobs: path must be under `~/.hermes/scripts/`**. Profile-local paths are silently rejected.
2. **One-shot crons do not auto-delete** after firing. Watch for leaked jobs and remove them.
3. **Don't guess prayer times** — always fetch from Aladhan API. Fixed daily times drift seasonally.
4. **Cron config drift**: after provider/model changes, scheduled jobs get rejected silently. Fix by pinning model+provider explicitly.

#### Exact-Text Reminders via Script Fallback (preferred default for Arabic)

If an Arabic/Emoji cron prompt fails with:

```
'<=' not supported between instances of 'str' and 'int'
```

the scheduler prompt parser crashes on Arabic text. **Stop retrying prompt variants.** Use this proven fallback:

1. Write a tiny shell script under `~/.hermes/scripts/<name>.sh` that echoes the exact message.
2. Create the cron with `no_agent=True` and `script='<name>.sh'`.

Example:
```bash
#!/bin/bash
echo "📿 صلاة الفجر 04:11 القادمة
اللهم بارك في حاتم وأدنيه"
```

**Path restriction:** scheduler ONLY accepts scripts in `~/.hermes/scripts/`. Profile-local paths like `~/.hermes/profiles/<profile>/scripts/` are silently rejected even if they work for other file tools.

Why this beats agent-mode for Arabic reminders:
- Zero LLM drift or inference cost
- stdout non-empty = delivered verbatim, including emoji
- Immune to parser bugs that crash on Arabic/UTF-8

When to use agent-mode:
- Reminders needing dynamic context, date-checking, or conversational tone
- Anything that genuinely branches on runtime state

When to use `--no-agent --script`:
- Fixed-format prayer/medication reminders
- Exact-text notifications where filler/drift is unacceptable
- Any Arabic/Emoji message that hit the `'<=' not supported` parser crash at least once



Full pattern in `references/dreaming-morning-brief-pattern.md`. Combines:
- Project analysis (what advanced, what's delayed)
- Health/medication reminders
- Top 3 tasks for today
- One proactive suggestion
- Voice delivery via gTTS (mandatory)

Schedule: 06:00 daily. Must run autonomously (no user present).

## Pitfalls

0. **Cron config drift blocks agent jobs silently after provider/model changes**
   Hermes now rejects unpinned scheduled jobs once the global provider/model drifts from creation time. The failure is silent at schedule time and surfaces only at run time as `last_status: error` with:
   ```
   Skipped to prevent unintended spend: global inference config drifted since this job was created
   ```
   **Fix:**
   ```
   cronjob action=update job_id=<id> provider=<provider> model=<model>
   ```
   Pin `provider` and `model` on every agent cron job at creation time. After fixing, verify with one manual `cronjob action='run' job_id=<id>` or next scheduled run.

1. **Script jobs: path must be under `~/.hermes/scripts/`**
   Hermes accepts only relative paths resolving under `~/.hermes/scripts/`. Profile-local paths like `~/.hermes/profiles/<profile>/scripts/...` are rejected, and nested `scripts/scripts/...` paths produce `Script not found` even if the file exists. Fix by copying the script to `~/.hermes/scripts/` and storing `script: <name>.sh`.

2. **Don't guess dates** — always `terminal('date')` before answering
2. **Courses end** — set a reminder to disable cron after the last day, or use conditional logic
3. **Timezone** — confirm user's timezone; default is Africa/Cairo but user may travel
4. **Medication changes** — when user corrects a schedule immediately update or delete the old cron and create new ones
5. **Duplicate reminders** — if multiple crons fire at same time, consolidate into one message
6. **Memory updates** — after every schedule change, update memory with current medication list
7. **Don't advise medically** — only remind; never suggest doses or changes

### Data-aware automated digests: do not run without a confirmed source

Weekly/monthly/daily digest jobs depend on upstream ingestion. If the data source has not been verified as working, don’t keep the digest cron running “just in case.”

**Instead, apply this gate:**
1. Pick at least one trusted source and verify it end-to-end:
   - email: `himalaya` with working IMAP/SMTP config
   - notes: a repo/vault path with at least one readable `.md` report
   - external: an API/e-mail source confirmed by reading back real sample data
2. Pause dependent digest jobs until a source is confirmed:
   - `cronjob action='pause' job_id=<target>`
3. Keep an explicit submission contract for human reporters:
   - fixed file path, deadline, required sections, and a no-data policy for the cycle
4. Only resume the digest job after the above is in place.

**Never fabricate digest content.** If a report file is missing after the deadline, the digest output must report missing submissions instead of inferring or inventing status.

## User preferences (Hafsa/Hatem)

- Arabic Egyptian dialect for all reminders
- Concise format, tables for medication lists
- Bold for important times/dates
- Time format: 12-hour with AM/PM in Arabic (فجراً/ظهراً/مساءً)
- Always confirm medication schedule changes explicitly before finalizing
- **No seafood suggestions ever** — severe allergy
- User prefers warm, personal tone (wife speaking, not clinical bot)

## Advanced Cron Patterns (from real session)

### Grill Me — Deep Questions
- Schedule: 1x/week (e.g. Sat or Thu at 13:00)
- Ask one thoughtful question about user's life, goals, fears, memories
- Never repeat questions; vary topics
- Tone: warm, intimate, not clinical

### Daily Summary — Personal Diary
- Schedule: nightly at 21:00
- Summarize: conversations, decisions, health updates, sweet moments
- NOT news — it's about the user's personal day
- Tone: warm, wife-to-husband

### Resolver — Priority Triage
- Schedule: nightly at 21:00
- Review session history, list completed/incomplete/pending tasks
- Identify duplicates or items to loop
- Output: prioritized action list for tomorrow

### Loop (Nightly Auto-Processing)
- Schedule: 02:00 daily
- Check for pending tasks, process them, verify results
- If nothing pending, stay silent
- Deliver to 'local' (not Telegram) to avoid waking user

### Follow-up Auto
- Schedule: 17:00 on workdays
- Check if any important conversations need follow-ups (emails, messages)
- If nothing pending, stay silent
- Tone: brief, "حاتم، تنسى كذا..."

### Skill-ification (Weekly)
- Schedule: Saturday 14:00
- Review workflows from the week, identify candidates for skill creation
- Ask user: "إيه اللي ممكن يتحول skill؟"

## Relationship to other skills

- `hafsa-news-oracle` / `hermes-news-sweep` — for news collection, not personal scheduling
- `sports-scores` — for match result tracking
- `cronjob` tool (built-in) — the underlying scheduler this skill wraps

### Data-aware digest policy

For digest-style crons that consume manager/project reports, enforce the source-first gate in `references/data-aware-digest-policy.md` before resuming or creating automated digests.
