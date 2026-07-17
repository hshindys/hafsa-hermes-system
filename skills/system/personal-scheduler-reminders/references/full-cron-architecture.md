# Full Cron Architecture — Hafsa/Hatem Household

> Reference: all cron jobs created as of 25 Jun 2026 session.

## Active Cron Jobs (11 total)

| # | Name | ID | Schedule | Deliver | Purpose |
|---|------|----|----------|---------|---------|
| 1 | Date & Time | 3751d7690b88 | 05:00 daily | telegram | Arabic day + Gregorian + Hijri + time |
| 2 | AM Meds | 8bc8125d26a1 | 05:30 daily | telegram | كونكور + نيكسام + بيوتك |
| 3 | بيوتك | 00266f6ad638 | 10:30 daily | telegram | Only during 24-27 Jun course |
| 4 | Health Check | e0185fde789c | 10:00 Tue/Fri | telegram | BP, glucose, mood, pain check |
| 5 | Grill Me | 9e152e858f97 | 13:00 daily | telegram | Deep question to Hatem |
| 6 | Loop (nightly) | 2942a4d348d7 | 02:00 daily | local | Auto-process pending tasks |
| 7 | Follow-up | 075ab9e4f9ad | 17:00 workdays | telegram | Pending follow-ups reminder |
| 8 | Resolver | 0e0658c60c5d | 21:00 daily | telegram | Priority triage from session history |
| 9 | Daily Summary | e675373edfca | 21:00 daily | telegram | Personal day summary |
| 10 | Skill-ification | ef92874e3b7f | 14:00 Saturday | telegram | Weekly skill review |
| 11 | PM Meds | 8ebea3cd11d2 | 22:30 daily | telegram | Evening medications |

## Timing Map

```
02:00  🔄 Loop (silent/local)
05:00  📅 Date & Time
05:30  💊 AM Meds
10:00  🏥 Health Check (Tue/Fri only)
10:30  💊 بيوتك (course-limited)
13:00  🤔 Grill Me
14:00  🛠️ Skill-ification (Saturday only)
17:00  📭 Follow-up (workdays only)
21:00  ⭐ Resolver + 💕 Daily Summary
22:30  🌙 PM Meds
```

## Design Principles

- **No overlap at same minute** — each cron has unique time
- **Silent when nothing to report** — most crons stay quiet if no action needed
- **Course-limited meds** — conditional logic in prompt, no manual disable needed
- **Warm tone** — all messages in Egyptian Arabic, wife-to-husband style
- **Health data** — never used for medical advice, only tracking/reminders
