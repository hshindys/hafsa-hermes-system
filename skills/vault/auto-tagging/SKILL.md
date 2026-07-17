---
name: auto-tagging
title: Auto-Tagging Skill — حفصة 🤖
description: يُستخدم تلقائيًا عند إنشاء أو تعديل أي ملف في الخزنة — يضيف tags المناسبة تلقائيًا بناءً على المحتوى والمجلد.
version: 1.1.0
---

# Auto-Tagging Skill — حفصة 🤖

## الهدف
عندما يُنشأ أو يُحدَّث ملف `.md` في `/home/hatem/Documents/Hafsa`، يتحقق تلقائيًا من المحتوى ويضيف الـ tags المناسبة في Frontmatter.

## القواعد

### 1. المجلد (Folder → preset tags)
- `📅 اليوميات/` → `daily`
- `03-World-of-Kron/` أو `📚 World of Kron/` → `kron`, `novel`, `worldbuilding`
- `03-World-of-Kron/Entities/` → `kron`, `novel`, `worldbuilding`, `entities`
- `03-World-of-Kron/Relations/` → `kron`, `novel`, `worldbuilding`, `relations`
- `03-World-of-Kron/Archive/` → `kron`, `novel`, `worldbuilding`, `archive`
- `📚 Knowledge/World Cup 2026` أو فرع منها → `world-cup`, `egypt`, `football`
- `📚 Knowledge/` → `knowledge`, `reference`
- `🚀 Projects/` → `projects`, `system`
- `Reports` أو `📊 Reports/` أو `تقارير/` → `reports`
- `02-Work-System/` → `work`, `system`
- `scripts/` أو `.hermes-cron/` أو `Archive/` → يتجاهل

### 2. المحتوى (Content → intelligent tags)
إذا كان المحتوى فيه:
- **رواية / قصة / فصل / شخصية** → أضف: `novel`, `fiction`
- **أدوية / دواء / كونكور / نيكسام / إكسفورج / سينجاردي / أسبرين / أتوريزا / كيوف** → أضف: `meds`, `hatem-health`
- **World Cup / كأس العالم / مصر / مباراة / فراعنة** → أضف: `world-cup`, `egypt`, `football`
- **Hermes / Discord / Telegram / Slack / أتمتة** → أضف: `hermes`, `automation`
- **سليم / سليمة / صفى / زليخة / نبوكات / أريوس / بنت سلمار / طارق / صفا** → أضف `characters`
- **Memory.md / memory** → أضف: `memory`
- **Index.md / الفهرس** → أضف: `index`, `vault-management`
- **Daily Brief** → أضف: `brief`, `world-cup`

### 3. شكل Frontmatter
- نستخدم مصفوفة tags بخط واحد قدر الإمكان بدون تكرار: `tags: ["kron", "novel", "worldbuilding"]`
- لا تحذف tags موجودة مسبقًا — فقط تضيف الجديد
- لا تفرض tags على الملفات داخل `Archive` أو backup/scripts

### 4. طريقة التنفيذ
1. اقرأ الملف
2. حدد المسار → Tags افتراضية من المجلد
3. افحص المحتوى → Tags ذكية إضافية
4. حدث Frontmatter مع قائمة موحدة بدون تكرار

### 5. تشغيل الدفعات
- تشغيل آمن على vault دفعة واحدة فقط عند الطلب
- استثناء المجلدات: `Archive`, `backups`, `.hermes-cron`, `tmp`
- يعتبر الكلمة اللاتينية ذات معنى فقط إذا لم تكن matching قائمة noise ثابتة
- لا يعيد كتابة ملفات ما عدا `tag_frontmatter`

## Support Files
- `scripts/auto-tagger.py`: سكريبت بايثون لتطبيق القواعد على ملف واحد
- `scripts/auto-tag-watcher.sh`: سكريبت bash يمسح الملفات المعدلة في آخر ساعة ويشغل auto-tagger

