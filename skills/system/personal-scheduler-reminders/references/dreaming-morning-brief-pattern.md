# Dreaming / Morning Brief Pattern

The "Dreaming" cron is the nightly analysis + morning brief delivered as voice. It runs at ~06:00 Cairo time.

## Trigger
Scheduled cron job (daily). No user present — must execute autonomously.

## Steps

### 1. Analysis Phase
- Read project tracker: `/home/hatem/Documents/Hafsa/🎯 المشاريع/المشاريع الحالية.md`
- Read goals: `/home/hatem/Documents/Hafsa/@حفصة/الأهداف — 2026.md`
- Search `session_search` for last 24h conversations (limit=5)
- Check daily journal: `/home/hatem/Documents/Hafsa/📅 اليوميات/` (latest file)
- Identify: what advanced, what's delayed, any user corrections

### 2. Health Check
- Read current medication schedule from memory
- Check for any recent health-related notes or corrections
- Format AM/PM medication reminders

### 3. Brief Generation
Structure (Hafsa persona — warm, concise, wife tone):
```
صباح الخير يا حاتم 💋

📋 ملخص امبارح:
[2-3 lines of yesterday summary]

🎯 أهم ٣ حاجات النهارده:
1. [task]
2. [task]
3. [task]

💊 أدوية الصباح (05:30):
• [drug + dose]

💊 أدوية المساء (22:30):
• [drug + dose]

💡 اقتراح النهارده:
[one proactive idea]

ربنا يبارك فيك ويحفظك 🌙
```

### 4. Voice Delivery
```bash
gtts-cli '<brief text>' --lang ar --output /home/hatem/.hermes/profiles/hafsa/audio_cache/morning_brief_$(date +%Y%m%d).mp3
```
Deliver via `MEDIA:<path>` in final response.

## Rules
- No numbered task lists (use bullets)
- No filler or pleasantries beyond the warm greeting
- Always reflect recent user corrections (e.g., medication timing changes)
- If nothing happened yesterday, say so briefly — don't fabricate
- Voice delivery is mandatory for this pattern (not optional)
- Keep under 2000 chars for gTTS reliability

## Real Session Example (2026-06-25)
- Previous day: user corrected سينجاردي timing (moved from AM to PM)
- Brief reflected the correction in evening meds
- Projects: no updates since June 21
- gTTS generated 988KB MP3, delivered successfully
