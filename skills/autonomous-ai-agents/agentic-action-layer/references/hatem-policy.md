# Hatem-Specific Policy Notes — Action Layer

## Vault Roots
- Lola: `/home/hatem/Documents/Lola`
- Dina: `/home/hatem/Documents/Dina`
- Shared: `/home/hatem/Documents/Hatem Nad`

## Forbidden Patterns
- seafood: بحر، سمك، جمبري، كراب، سلمون، تونة، seafood
- medical advice regex: نصيحة طبية|تشخيص|أعط دواء|medical advice
- destructive ops: DELETE DATABASE|DROP TABLE|rm -rf /|format\s+c:
- secret leakage: api[_-]?key\s*[:=]|token\s*[:=]|password\s*[:=]

## User Context
- Timezone: Africa/Cairo (UTC+3)
- Medications morning 07:00: كونكور بلس 5 + نيكسام 40
- Medications evening 22:30: إكسفورج 10 + سيجاردي 10 + أسبرين بروتكت + أتوريزا 10 + أوميجا 3
- Prayer times Cairo: Fajr 04:18, Dhuhr 13:00, Asr 16:37, Maghrib 19:59, Isha 21:30
- Allowed reminders/jobs must use Cairo times.
- Terse continuation responses: "ok", "اعمل", "طبق", "تمام" => execute immediately, no further confirmation.

## Output Discipline
- Arabic only, RTL, no inline English, no weird symbols.
- No medical advice; medication reminders only.
- No seafood suggestions.
