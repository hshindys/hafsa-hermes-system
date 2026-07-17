---
name: self-scaffolding
description: |
  طبق فكرة Ornith 1.0: الموديل يكتب/يعدل الـ harness بتاع المهمة بنفسه حسب السياق.
  يستخدم لإنشاء أدوات بسيطة (weather, news, integrations) ديناميكياً.
version: 0.1.0
---

# Self-Scaffolding Skill

## الفكرة
basata على Ornith 1.0: الموديل بيكتب الـ scaffold (code + config) بنفسه حسب المهمة،
وبعدين يستخدم الـ scaffold ده عشان ينفذ المهمة.

## المراحل
1. **Analyze** — افهم المهمة وحدد الأدوات المطلوبة
2. **Generate** — اكتب الكود/الconfig للـ harness
3. **Verify** — اختبر إن الـ harness شغال
4. **Execute** — استخدم الـ harness لتنفيذ المهمة

## الاستخدام
- `generate_harness(task_description)` — يكتب harness جديد
- `refine_harness(task, feedback)` — يعدل harness موجود بناءً على النتيجة
- `execute_with_harness(task, harness_path)` — ينفذ مهمة باستخدام harness

## هيكل الـ Harness
كل harness بيكون ملف Python بسيط في `/tmp/harnesses/` مع:
- `run()` function — بتاخد المدخلات وترجع النتيجة
- `config` dict — الإعدادات (API keys, endpoints)
- `validate()` function — بتشغل اختبارات سريعة

## Fallback policy
- If `execute_code` is unavailable, use `terminal` + `python3 -c` / `python3 /path/to/harness.py`.
- Always write harnesses to `/tmp/harnesses/` before running them.

## API pitfalls
- **Open-Meteo `daily` encoding:** do not pass `daily` as a list value in a dict passed to `urllib.parse.urlencode`; that joins with commas and returns HTTP 400. Use repeated `daily=...` params instead:
  - Good: `urllib.parse.urlencode([("daily","a"),("daily","b")])`
  - Bad: `urllib.parse.urlencode({"daily":["a","b"]})`
- **Open-Meteo date-window mutual exclusion:** `forecast_days` is mutually exclusive with `start_date` and `end_date`. Pick one style per request:
  - Relative window: `forecast_days=N`
  - Fixed window: `start_date=YYYY-MM-DD` + `end_date=YYYY-MM-DD`, without `forecast_days`
  - Mixing them returns `Parameter 'forecast_days' is mutually exclusive with 'start_date' and 'end_date'`.
- In this environment, add a Cairo weather reference note under `references/open-meteo.md` when possible; if support-file writes are restricted, carry the needed facts inside this SKILL.md instead.

## أمثلة
- Weather harness: يتصل بـ Open-Meteo API بدون مفتاح
- News harness: يجيب أخبار من RSS/Atom feeds
- Integration harness: يربط بين tools مختلفة
