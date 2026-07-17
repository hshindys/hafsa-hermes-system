# Hatem's Current Medication Schedule (2026)

> Reference file — update when medications change. Always verify dates with `terminal('date')` before use.

## Active Schedule (as of 29 Jun 2026)

| Time | Medication | Dose | Notes |
|------|-----------|------|-------|
| 10:30 صباحاً | بيوتك 500 (Biotic) | 500mg | Daily maintenance — antibiotic course (24-27 Jun) has ENDED |
| 22:30 مساءً | إكسفورج (Exforge) | 10mg | Daily |
| 22:30 مساءً | سينجاردي (Singulair) | 10mg | Daily |
| 22:30 مساءً | أسبرين بروتكت | — | Daily |
| 22:30 مساءً | أتوريزا (Atorvastatin) | 10mg | Daily |
| 22:30 مساءً | أوميجا 3 | 69 | Daily |

## Stopped / Not Currently Used
- كونكور بلس (Concor Plus) 5mg — **متوقف**
- نيكسام (Nexium) 40mg — **متوقف**

## Conditions
- T2D (Type 2 Diabetes)
- HTN (Hypertension)
- Benign brain tumor
- Severe allergy to ALL seafood (fish, shrimp, crab) — NEVER suggest seafood

## Notes
- User prefers Egyptian Arabic (عامية) for reminders
- Timezone: Africa/Cairo UTC+3
- Evening meds are at 22:30, NOT 10:30 PM (cron uses 24h)
- Morning meds list currently short: only biotics remaining from the course

## Course End Notes
- بيوتك antibiotic course ended 27 Jun 2026
- Cron job `00266f6ad638` now silently fires after course end — keep active in case schedule changes
- Reference this file before changing any bedo meds

## Multi-Round Correction Pattern (from this session)
1. نيكسام moved from PM → AM
2. بيوتك frequency: twice daily (10:30 + 22:30) not once
3. بيوتك duration: 4-day course (24-27 Jun)
4. Course start date: \"امبارح\" = 24 Jun
5. كونكور/نيكسام confirmed stopped by user

**Lesson:** After the FIRST correction, always re-present the full schedule as a table and confirm BEFORE creating/updating crons.

## Cron Jobs Created
- 00266f6ad638: بيوتك reminder @ 10:30 daily
- 8ebea3cd11d2: Evening meds reminder @ 22:30 daily
