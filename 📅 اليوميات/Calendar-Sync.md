# 📅 تقويم الأسبوع (Google Calendar ← Hermes)

> آخر محاولة: 2026-08-16 06:30 القاهرة

⚠️ **فشلت المزامنة — لم تُجلب أي أحداث.** السبب: انتهت صلاحية رمز الدخول (refresh token) الخاص بـ Google (`invalid_grant`). هذا ليس غياب أحداث، بل خطأ في المصادقة.

🔧 **للإصلاح (مطلوب تسجيل دخول يدوي من حاتم):**
```bash
cd "C:/Users/hshin/AppData/Local/hermes/skills/productivity/google-workspace/scripts"
python setup.py
```
ثم أعد تشغيل:
```bash
python "C:/Users/hshin/hafsa-hermes-system/scripts/sync_calendar_to_vault.py"
```
