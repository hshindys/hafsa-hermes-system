# Medication Schedule Corrections Log

Track user corrections to medication timing/dosage so briefs always reflect the current schedule.

## Corrections

### 2026-06-24: السينجاردي مساء مش صباحا
- **Before:** سينجاردي was listed under morning medications
- **After:** سينجاردي moved to evening (22:30)
- **Corrected schedule:**
  - Morning (05:30): كونكور بلس 5mg + نيكسام 40mg
  - Evening (22:30): إكسفورج 10mg + سينجاردي 10mg + أسبرين بروتكت + أتوريزا 10mg + أوميجا 3 69
- **Source:** User correction via Telegram session "تصحيح موعد السينجاردي بين الزوجين"

### 2026-06-25: نيكسام رجع للصباح + بيوتك بدأ
- **Before:** نيكسام was at night (was moved in a previous session)
- **After:** نيكسام back at morning (05:30), بيوتك 500 started June 24 (4-day course)
- **Corrected schedule:**
  - 05:30: كونكور بلس 5mg + نيكسام 40mg
  - 10:30: بيوتك 500 (فقط 4 أيام: 24، 25، 26، 27 يونيو)
  - 22:30: إكسفورج 10mg + سينجاردي 10mg + أسبرين بروتكت + أتوريزا 10mg + أوميجا 3 + بيوتك 500
- **Source:** User correction via Telegram session

### 2026-06-25: اليوم التاني مش التالت + تحذير من حساب الأيام
- **Before:** حسبت اليوم 25 يونيو = اليوم التالت من بيوتك
- **After:** اليوم 25 يونيو = اليوم التاني (بدأ 24 يونيو)
- **Rule:** Always verify date with `terminal('date')` before calculating day counts. Do NOT guess dates.

### 2026-06-25: تحذير من تخمين الوقت/التاريخ
- **Rule:** لا تخمن أبداً. استخدم `terminal('date')` للتحقق من التاريخ والوقت.
- **Reason:** حدث خطأ في حساب أيام الكورس — الفرق يوم واحد يمكن يسبب جرعة زيادة أو ناقصة.

## Rule
Always read memory at runtime before generating medication reminders. Never hardcode. If a correction is received, update memory immediately and reflect in next brief.

## Current Verified Schedule (2026-06-25):
- **05:30:** كونكور بلس 5mg + نيكسام 40mg
- **10:30:** بيوتك 500 (آخر جرعة: 27 يونيو)
- **22:30:** إكسفورج 10mg + سينجاردي 10mg + أسبرين بروتكت + أتوريزا 10mg + أوميجا 3 + بيوتك 500
