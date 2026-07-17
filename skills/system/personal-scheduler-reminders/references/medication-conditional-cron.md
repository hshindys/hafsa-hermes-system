# Medication Conditional Cron Pattern

## Pattern: Finite Course Reminder

When a user takes a medication for a limited number of days (e.g., 4-day antibiotic course), the cron job must check the date before sending a reminder.

### Implementation

Create a cron job with conditional logic in the prompt:

```
Action: cronjob
Schedule: "30 10 * * *" (daily at 10:30)
Prompt: "Check today's date using terminal('date +%Y-%m-%d'). 
If today is between [start_date] and [end_date] (inclusive):
  Send a brief reminder (Arabic Egyptian dialect) for [drug_name] [dose].
If outside this range:
  Reply SILENTLY (do not send any message to the user)."
```

### Real Example: بيوتك 500 (4-day course, 24-27 June 2026)

Two daily doses at 10:30 and 22:30:

| Cron | Schedule | Conditional Logic |
|------|----------|-------------------|
| AM dose | `30 10 * * *` | Only if date ≤ 2026-06-27 |
| PM dose | `30 22 * * *` | Only if date ≤ 2026-06-27 |

### Key Rules

1. **Always include the date check in the prompt** — don't rely on the agent "remembering" the end date
2. **Use SILENT reply after course ends** — not an error, just no output
3. **Update memory immediately** when user changes schedule
4. **Confirm changes** — read back the full updated schedule before creating crons
5. **Handle corrections gracefully** — user may correct timing/dose multiple times; delete old crons and create new ones

### Multi-Medication Schedule Example

For a user with multiple medications at different times:

```
05:30 → كونكور بلس 5mg + نيكسام 40mg (daily, no end date)
10:30 → بيوتك 500 (conditional: 24-27 June 2026 only)
22:30 → إكسفورج 10mg + سينجاردي 10mg + أسبرين + أتوريزا + أوميجا (daily)
22:30 → بيوتك 500 (conditional: same as AM)
```

Create separate cron jobs for each time slot, each with its own conditional logic.
