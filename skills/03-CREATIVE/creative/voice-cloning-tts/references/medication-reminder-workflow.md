# Medication Reminder Workflow — From Video Use Case

Pattern from 2026-06-25 session: using cron jobs for medication reminders with allergy awareness.

## When to Apply

Use this pattern when the user wants:
1. Scheduled medication reminders
2. Course-based reminders (e.g., "take X for 4 days")
3. Health check-in prompts
4. Follow-up reminders

## Steps

### 1. Extract Medication Schedule

```
Read SOUL.md / user profile / memory:
- Drug names
- Doses
- Timing (AM/PM)
- Course duration (if limited)
- Allergies (CRITICAL)
```

### 2. Create Cron Jobs

For each medication time slot:
```
Cron schedule: "05:30 daily" / "22:30 daily"
Prompt: "Remind user of X at Y time"
```

For course-based:
```
Prompt: "Check if date is between START and END. If yes, remind. If no, skip silently."
```

### 3. Allergy Safety Check

```
Before any health response:
1. Check SOUL.md for allergies
2. NEVER suggest allergen-containing items
3. Flag in user-visible reminders:🚫 ممنوع: <allergen>"
```

### 4. Warm Reminder Tone (Arabic Egyptian)

```
✅ "وقت الكونكور يا حبيبي 💊"
✅ "ماتنساش النيكسام الساعة دلوقتي"
❌ "يجب تناول الدواء في الوقت المحدد" (too clinical)
```

## Example: Complex Schedule

User has:
- Morning: كونكور 5mg + نيكسام 40mg at 05:30
- Midday: بيوتك 500mg at 10:30 (course: 4 days)
- Evening: Multiple meds + بيوتك at 22:30

Created 4 crons:
1. 05:30 daily — morning meds
2. 10:30 daily (date-gated) — بيوتك
3. 22:30 daily — evening meds
4. Custom — health check 2x/week

## Pitfall: Course End Date

Always include date check in prompt:
"Check today's date. If it's between [start] and [end], send reminder. After [end], silently skip."

## Related

- health-reminder-cron skill
- world-recipes-vault skill
