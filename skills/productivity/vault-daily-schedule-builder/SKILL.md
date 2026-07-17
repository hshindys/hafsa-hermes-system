---
name: vault-daily-schedule-builder
description: ينشئ جدول يومي مخصص في ملاحظة الخزنة اليومية (Daily Note) يجمع مواقيت الصلاة + أنشطة مخصصة + أذكار من حصن المسلم. تشغيل تلقائي أو يدوي.
_triggers:
  - daily_vault_schedule
  - prayer_times
  - daily_routine
  - spiritual_schedule
  - adhkar_schedule
  - aladhan_api
  - vault_upsert
  - markdown_table_schedule
---

# vault-daily-schedule-builder

ينشئ جدول يومي مخصص في ملاحظة الخزنة اليومية يجمع مواقيت الصلاة + أنشطة مخصصة + أذكار من حصن المسلم.

## متى تستخدم
- عند بناء سكربت يجيب مواقيت صلاة + يبني جدول أوقات مخصص
- عند دمج scheduled items (قرآن، أذكار، كتابة، مكالمات) داخل ملاحظة يومية
- عند استخدام upsert-into-note pattern لمنع التكرار اليومي
- عند ربط Daily Note بـ Aladhan API + كاش يومي

## المكونات الأساسية

### 1. Source of truth: TOML config
```toml
[location]
city = "Giza"
country = "Egypt"
latitude = 30.0131
longitude = 31.2089
timezone = "Africa/Cairo"
calculation_method = 5

[vault]
path = "/home/hatem/Documents/..."
daily_note_pattern = "Daily/{date}.md"
section_header = "## الروتين الروحي"

[schedule]
quran_minutes_after_fajr = 0
quran_duration_minutes = 30
morning_adhkar_minutes_after_fajr = 20
asma_minutes_after_fajr = 25
writing_minutes_after_asr = 0
writing_duration_minutes = 45
family_call_minutes_after_maghrib = 15
evening_adhkar_minutes_after_maghrib = 5
sleep_time = "23:00"
sleep_adhkar_minutes_before_sleep = 15

[cache]
dir = "/home/hatem/.hermes/cache"
```

### 2. Prayer times + daily cache
- يستخدم Aladhan API: `https://api.aladhan.com/v1/timings/{DD-MM-YYYY}`
- كاش يومي محلي: `prayer_times_{YYYY-MM-DD}.json`
- الـ API بيرجع أحياناً `"04:11 (EEST)"` — خوار بسيط: `timing[:5]`

### 3. Time arithmetic
```python
def add_minutes(t: str, minutes: int) -> str:
    dt = datetime.strptime(t, "%H:%M") + timedelta(minutes=minutes)
    return dt.strftime("%H:%M")
```

### 4. Upsert-into-note (منع التكرار)
```python
def upsert_into_note(vault, pattern, date, header, block):
    path = vault / pattern.format(date=date.strftime("%Y-%m-%d"))
    path.parent.mkdir(parents=True, exist_ok=True)
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    if header in content:
        return path  # موجود بالفعل، ماكررش
    sep = "\n\n" if content and not content.endswith("\n\n") else ""
    path.write_text(content + sep + block, encoding="utf-8")
    return path
```

### 5. Multi-line items في markdown
```python
def format_multi(title, items):
    lines = [title]
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines)
```
وفي الـ render: استخدم `if "\n" in label:` لعمل indented sub-lines.

## الأذكار — جاهزة للاستخدام
راجع `references/adhkar-al-husna.md` للقوائم الكاملة (استيقاظ، صباح، مساء، نوم).

## التشغيل التلقائي
ب Macdonald أضف cron job يومي يشغل السكربت بعد صلاة الفجر:
```bash
python3 /path/to/daily_routine.py
```

## الأسماء الحسنى اليومية
- يتم اختيار اسم تلقائي حسب يوم السنة: `day_index % len(ASMA_AL_HUSNA)`
- نفس الدعاء: `DUAS[day_index % len(DUAS)]`

## Vault path considerations
- دائمًا استخدم `Path.expanduser()` على المسارات
- دائمًا `mkdir(parents=True, exist_ok=True)` قبل الكتابة
- الـ encoding لازم يكون `utf-8` عشان العربية

## Pitfalls
- `tomllib` متوفر فقط Python 3.11+ — لو قديم، `pip install tomli`
- لا تكرر القسم في اليوم إذا شغّلت السكربت مرتين — upsert يحمي من هذا
- مواقيت الصلاة اليومية تتغير مع الفجر — لازم تعيد تشغيل السكربت كل يوم
