---
name: vault-organization
description: استخدم عند تنظيم الخزنة، إنشاء مشاريع فرعية مثل الأهلي/World Cup، تحديد vault routing، تجنب التكرار، وبناء Overview.md قابل للبحث. تستخدم أيضاً عند تنفيذ PARA/PCM restructuring أو دمج مسارات مكررة بعد هجرات vault.
---

# Vault Organization / PARA-PCM Alignment

## متى نستخدم هذا المهارة
- تنظيم الخزنة بعد إضافة مشروع جديد
- توحيد الروتين routing + الفهرس
- تصميم بنية مشروع كروي/متابعة داخل Obsidian
- تنظيف التكرارات بين المجلدات

## الهيكل العام المقبول — OODA + PARA/PCM

### الخيار 1: OODA
```
/00-Inbox/
/01-Projects/
/02-Knowledge/
/03-Archive/
/04-System/
```

### الخيار 2: PARA/PCM
```
/01-Projects/
  AI-CFO-Monitor/
  Al-Ahly/
  Hermes/
/02-Areas/
  Work-System/
/03-Resources/
  World Cup 2026/
  Knowledge/
  Misc/
/03-World-of-Kron/
/Archive/
📅 اليوميات/
Religion/
scripts/
tmp/
```

## قواعد التأسيس
1. كل مشروع فرعي يبدأ بـ `Overview.md`
2. المباريات: `Matches/Log.md` + `Matches/Schedule.md`
3. البطولات: للمسابقة ملف单独 في `Competitions/`
4. المصدر الرسمي يُذكر داخل كل ملف في الـ frontmatter أو بقسم المصادر
5.Dataview جوهOverview لاستخراج:آخر مباراة + القادم + ملخص

## Vault Routing
- أضف كل project route فيIndex.md + Hafsa Vault.md
- استخدممسار موحد: project في`01-Projects/<ProjectName>/`
- World Cup canonical: `📚 Knowledge/World Cup 2026.md`

## تجنب التكرار
- World Cupنمرة واحدة فعلاً
- لا تكرر بنفس البيانات بينIndexوفهرسالآلي
- عند نقل مشروع من مسار خارجي للخزنة، احذف المجلد القديم أو انقله لـ Archive
- **PARA/PCM duplicate policy:** لا تترك نفس المحتوى في old+new paths. اختر المسار القياسي اللي رايح عليه، وانقل/احذف التاني.

## خطوات دمج المسارات المكررة (بعد هجرة/pcm-refactor)
1. شيك file existence قبل كل `mv`/`shutil.move`؛ collision = موجود في الوجهة؟ اسمح بالاستبدال/الحذف من المصدر
2. emoji/arabic duplicates مش بالضرورة identical paths: `📚 World of Kron/` ≠ `03-World-of-Kron/` — دمج المحتوى في المسار الجديد، واعمل trash/archive للقديم
3. بعد النقل: تحقق من الفراغ بـ `find /vault -maxdepth 2 -type d ! -path '*/.*' | sort`
4.Trash قديم: ما تحذفش فوراً — خلي مجلد مؤرخ إن كان اختيارك، أو `mv` تلقائي لـ `.trash` لو فيه file conflict
5. Empty-dir removal rule: use `any(p.iterdir())`, not `list(p.iterdir())`, because the latter keeps a generator-style reference that breaks `rmdir` checks in some states.
6. Cross-vault refactor: the same PARA/PCM merge pattern applies to sibling vaults. Apply identical cleanup sequentially: dedupe daily notes, unify Projects, unify Knowledge/Resources, merge Areas, validate empty folders.

## إجراءات إنذارية عند فشل النقل
- `mcp_filesystem_move_file` → `Parent directory does not exist` → أنشئ destination أولاً
- `mcp_filesystem_move_file` → `MCP server unreachable` → انتظر ~60s أو خلي حوالي `mv` بـ terminal/bash/python مباشر
- `Directory not empty` على مجلد قديم → معناها فيه ملفات متبقية أو collision؛ افحص بـ `find` ولوّح قسمة: موجودة في الوجهة → امسح المصدر، غائبة → انقلها
- لا تعيد نفس الأمر الجماعي مرتين — diagnosis أولاً ثم كمل يدوياً

## التحديث بعد المباريات
1. سجل النتيجة فيMatches/Log.md
2. حدّث ترتيب المسابقة في Competitions/<file>.md
3. عدّل المباراة القادمة فيMatches/Schedule.md
4. عبئOverview تلقائي من خلالDataview

## مصادر كرويةWITHarabic
- alahlyegypt.com/ar (الأهلي)
- kooora.com (عام)
- filgoal.com / goal.com / yallakora تحتاج browser بمساعدة proxy عند الحاجة

## تعليمات مهمة
- لا تحذف بيانات — انقل للأرشيف بدلاً من الحذف
- عند الت cleanse، استخدم مجلد مؤرخ: `أرشيف-تنظيف/<YYYY-MM-DD>/`
-記録 قاعدة RTL + صافي لملفات المشاريع الأدبية:wikilinks، النثر، frontmatter عربية فقط مالم يكن البرومبت مفصول بـ ```text```
-.Tag Schema لكل ملف: `[al-ahly, football, egypt, premier-league, caf, cup, overview]`
-.Match Log:tags`[al-ahly, football, matches, log]`
-.Update Index فوراً بعد أي إضافة مشروع

## Nightly Cron: تحديد النوتس الجديدة فعلاً
- ملاحظة اليوم الفارغة لا تعني automatically new-only batch.
- استخدم مزيج `recent_notes` + `find -newermt '1 day ago'` لتحديد الملفات المعدلة/الجديدة فعلاً قبل عدّها كـ “جديدة”.
- ما تحسبش المولدات التلقائية كإنتاج جديد إلا إذا فيه محتوى يدوي م-added نفس اليوم.

## Vault-Specific Quirks — Hatem Nad
- Canonical index filename is `00-فهرس-الخزنة.md`, not `00-Second-Brain-Index.md`; the latter may exist only in `04-Archive/old-indexes/`.
- World Cup tracker canonical path is `01-Projects/World Cup 2026.md`; do not treat older archive copies as authoritative when writing nightly updates.
- Daily notes may exist in both `📅 اليوميات/` and `05-Daily/`; prefer `📅 اليوميات/` for user-facing diary context unless specified otherwise.
- Orphan scans often return huge novel-related noise from `رواية-كرون/**`; unless asked, do not mass-relink novel files.
- Daily note may exist in `📅 اليوميات/` but may not exist for current date yet; if missing, record absence in report and do not fabricate.
- Vault search fallback: full-text search can fail on date-like tokens from vault paths, e.g. `mcp_vault_hatem_search query="2026-07-15"` failing with `no such column: 07`. Procedure: narrow query to non-numeric tokens, use term-based search, or pivot to `recent_notes` + filename inspection via terminal/path APIs.

## References
- `references/para-pcm-restructure.md` — تشخيص + before→after mapping من تنفيذ PARA/PCM فعلي على vault حفصة، 2026-07-11
- `references/kron-vault-cleanup-workflow.md`
- `references/al-ahly-project-template.md`
