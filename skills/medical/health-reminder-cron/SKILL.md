---
name: health-reminder-cron
description: >
  MUST USE when setting up scheduled medication reminders, health check-ins,
  or wellness notifications via cron jobs. Covers: medication schedules with
  time-based reminders, allergy/drug interaction awareness, health tracking
  prompts, and Arabic Egyptian dialect for warm spousal communication.
  Use when user mentions: medication reminder, health check, pill schedule,
  medication time, health tracking, daily check-in, تذكير أدوية, متابعة صحية.
---

# Health Reminder Cron — Medication & Wellness Reminders

Create scheduled cron jobs for medication reminders, health check-ins, and wellness tracking with warm spousal tone.

## When to use

- User wants medication reminders at specific times
- Setting up daily/weekly health check-ins
- Tracking blood pressure, blood sugar, or general wellness
- Reminding about medication courses (e.g., antibiotics for N days)
- Building a health monitoring system with cron jobs

## Architecture

```
User Profile (SOUL.md / memory)
├── Medications (name, dose, frequency, timing)
├── Allergies (SEVERE — must never suggest)
├── Conditions (diabetes, hypertension, etc.)
└── Health Check Schedule
    ↓
Cron Jobs Created
├── Morning meds (05:30)
├── Evening meds (22:30)
├── Course-based (e.g., بيوتك 4 days)
├── Health check-in (weekly)
└── Follow-up reminders
```

## Medication Reminder Pattern

### Step 1: Extract Medication Info

From user profile/memory, extract:
- **Drug name** (generic + brand if known)
- **Dose** (e.g., 5mg, 500mg)
- **Timing** (AM/PM, specific time)
- **Frequency** (daily, twice daily, course-based)
- **Special instructions** (with food, empty stomach)

### Step 2: Create Cron Job

```yaml
cron:
  schedule: "<time> * * *"
  prompt: |
    Remind <user> of medications:
    - <drug> <dose> at <time>
    - Check if course is still active (for limited courses)
    - Use warm spousal tone in Arabic Egyptian dialect
    - Include allergy warnings if relevant
```

### Step 3: Course-Based Medications

For medications taken for a limited number of days:

```
1. Create cron with daily schedule
2. Prompt checks date range before sending reminder
3. After course end date, disable/remove the cron
4. Update memory with course completion
```

## Allergy & Drug Interaction Awareness

### CRITICAL: Allergy Check

Before ANY health-related response:

1. **Check user profile for allergies** — SOUL.md / memory
2. **NEVER suggest** any medication, food, or substance the user is allergic to
3. **Warn explicitly** if something potentially dangerous is mentioned
4. **Flag in every reminder**: "ممنوع حاتم: <allergy>"

### Drug Interaction Awareness

When multiple medications are scheduled:
- Note potential interactions in the reminder
- Separate timing if needed (e.g., some meds AM, some PM)
- Flag any OTC items that might interact

## Health Check-In Pattern

### Weekly Health Check (Arabic Egyptian)

```
اسألي بالعربي المصري عن:
1. أي ألم جديد أو مختلف؟
2. ضغط الدم — قيسته؟ إيه الرقم؟
3. السكر — قيسته؟ إيه الرقم؟
4. النوم — إيه حاله؟
5. الأكل — في حاجة مش مناسبة أكلتها؟
6. المزاج — إيه حاله؟
```

**Tone:** Warm, spousal, not clinical. Use phrases like:
- "إيه أخبار صحتك يا حبيبي؟"
- "قولي إيه اللي بيضايقك"
- "خليني أتأكد إن كل حاجة تمام"

## Arabic Egyptian Dialect Guidelines

For medication reminders:
- Use "يا حبيبي" or "يا عمري" — warm spousal address
- Keep it brief: "وقت الكونكور يا حاتم 💊"
- Add emoji for visual clarity: 💊🌙⏰
- Avoid formal Arabic — use عامية مصرية
- Never use "أنا طبيب" — always frame as "تذكير" not "نصيحة طبية"

### Pitfalls

#### Restoring paused medication reminders
After profile/profile-switch updates, existing medication crons can end up paused with stale wording/date ranges. Fix pattern:
1. `cronjob action=list` and locate matching reminder jobs.
2. `cronjob action=update` with modernized prompt and schedule.
3. `cronjob action=resume` for each job.
Rule: prefer repair over creating duplicate new crons.

### 1. Medical advice vs. reminder
**WRONG:** "ده الدوا ده هيفيدك في كذا"
**RIGHT:** "وقت الدوا — خد كونكور 5mg"
**Rule:** NEVER give medical advice. Only remind about medications the user is already taking. Direct to doctor for any new symptoms.

### 2. Allergy oversight
**WRONG:** Suggesting fish oil when user has seafood allergy
**RIGHT:** Always cross-reference allergy list before any health mention
**Rule:** Keep allergy list in SOUL.md / memory and check before EVERY health-related response

### 3. Course end date
**WRONG:** Continuing to remind about a completed course
**RIGHT:** Track course dates in memory, check before each reminder
**Rule:** For course-based meds, always include date check in prompt

### 4. Timezone confusion
**WRONG:** Scheduling reminders in UTC when user is in UTC+3
**RIGHT:** Always use user's timezone (Africa/Cairo for Egyptian users)
**Rule:** Store timezone in memory, verify cron schedule matches

### 5. Duplicate reminders
**WRONG:** Creating multiple crons for same medication
**RIGHT:** Check existing crons before creating new ones
**Rule:** List crons first, update existing rather than creating duplicates

## See Also

- `references/medication-schedule-format.md` — Standard format for storing medication schedules
- `references/allergy-checklist.md` — Template for allergy tracking
- `internal-medicine-ai-diagnosis` — For clinical diagnosis discussions (NOT for reminders)
