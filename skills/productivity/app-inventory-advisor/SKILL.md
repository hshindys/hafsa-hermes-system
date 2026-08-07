---
name: app-inventory-advisor
description: "Recommend daily planner/calendar + app-handling for this Windows machine."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# جرد التطبيقات + توصية المخطط/التقويم (هذا الجهاز)

## التطبيقات المثبّتة (فحص 2026-08-07)
| التطبيق | الدور | ملاحظة |
|---------|------|--------|
| Obsidian 1.13.4 | خزنة المعرفة (Vault حفصة) | القاعدة الأساسية — كل الملاحظات هنا |
| OneDrive | مزامنة السحابة | الـ Vault متزامن منه (حذر: لا تضع أسرار فيه) |
| Jellyfin Server 10.11.11 | ميديا محلي | متصل بـ Hermes ✓ |
| Zen Browser / Edge | تصفّح | Zen للخصوصية، Edge افتراضي |
| Discord | تواصل | متصل بـ Hermes ✓ |
| qBittorrent 5.2.3 | تورنت | تحميل |
| ONLYOFFICE 9.4 | مستندات Office | بديل مجاني لـ Word/Excel |
| Node.js 24.19 | بيئة تشغيل | لتطوير الوكلاء/السكريبتات |
| Copilot / GitHub Copilot / Kimi | مساعدات AI | متاحة للاستشارة |
| Hermes Agent | المساعد الشخصي | أنا ✨ |

## توصية نظام التخطيط اليومي (Daily Planner + Calendar)
بما إن الخزنة على Obsidian ومتزامنة، **الأنسب**:
1. **التقويم:** ربط Obsidian بـ Google Calendar عبر plugin `obsidian-calendar` أو
   `google-calendar-sync` (نحتاج إعداد Google Workspace — عندك setup معلق).
   بديل خفيف: تقويم داخل الخزنة (ملف `📅 اليوميات/YYYY-MM-DD.md` — ده اللي بيعمله
   `daily_routine.py` أصلاً).
2. **المخطط اليومي:** `daily_routine.py` (شغال عبر cron 5 صباحاً) يولّد الجدول
   (صلاة + قرآن + أسماء الله + كتابة الرواية + أذكار + مكالمة عائلة). ده المخطط العملي.
3. **لو عايز تقويم بصري:** نضيف cron أسبوعي (Sunday 10 ص) يولّد "Knowledge Digest"
   وملخص أسبوعي في الخزنة.

## توصيات تحسين عامة
- لا تخلط أسرار (API keys, PATs) داخل مجلد OneDrive المتزامن — خليها في
  `AppData\Local\hermes\config` (عملنا كده مع Jellyfin ✓).
- استخدم Obsidian كـ single source of truth؛ Hermes يقرأ/يكتب منه.
- Node.js 24 متاح → مشاريع Lola/الوكلاء تشتغل محلياً.

## خطوات لاحقة مقترحة
- [ ] أكمل Google Workspace OAuth عشان نربط التقويم بصرياً.
- [ ] أضيف cron أسبوعي (Sunday digest) للخزنة.
- [ ] أربط `daily_routine.py` بمخطط أكثر تفصيلاً (مهام قابلة للتتبع).
