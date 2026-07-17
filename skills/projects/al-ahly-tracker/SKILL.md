---
name: al-ahly-tracker
description: متابعة مباريات النادي الأهلي المصري مباشرة في الخزنة. استخدم عند إضافة نتيجة مباراة/جدول/ترتيب/مصابين، أو تحديث Overview أو أي ملف في 01-Projects/Al-Ahly.
allowed-tools: vault-hafsa, terminal, web_search, browser_navigate
---

# Al-Ahly Tracker

## الغرض
نظام متابعة مركزية للأهلي داخل الخزنة. كل الملفات canonical في:
`/home/hatem/Documents/Hafsa/01-Projects/Al-Ahly/`

## هيكل المشروع الكامل
```
01-Projects/Al-Ahly/
Overview.md
Dashboard.md
Progress.md
Bases-View.md
Matches/
  Log.md
  Schedule.md
  Template-Match.md
Competitions/
  Premier-League.md
  CAF-Champions-League.md
  Cup.md
Squad.md
Staff.md
Injuries.md
H2H.md
Progression.md
Coach.md
News/
  Clips.md
Players/
  <player-name>.md
Assets/
  Al-Ahly-Logo.jpg
  Players/
  Staff/
.obsidian/
  templates/
    Al-Ahly-Match.md
```

## ملفات الأساس
- `Overview.md` — لوحة المعلومات + Dataview + لوجو
- `Dashboard.md` — لوحة شاملة بكل الأقسام
- `Progress.md` — تقدم الموسم + شريط التقدم
- `Bases-View.md` — Bases view للمباريات + القائمة
- `Matches/Log.md` — سجل المباريات
- `Matches/Schedule.md` — جدول المباريات القادمة
- `Matches/Template-Match.md` — قالب Templater للمباريات
- `Competitions/Premier-League.md` — الدوري المصري
- `Competitions/CAF-Champions-League.md` — CAF
- `Competitions/Cup.md` — كأس مصر/السوبر
- `Squad.md` — القائمة الحالية
- `Staff.md` — الجهاز الفني والإداري
- `Injuries.md` — الإصابات والإنذارات
- `H2H.md` — المواجهات التاريخية
- `Progression.md` — تطور الترتيب جولة بجولة
- `Coach.md` — إحصائيات المدرب
- `News/Clips.md` — روابط + ملخصات
- `Players/<player-name>.md` — ملف إحصائي لكل لاعب

## way_of_work
### قبل أي تعديل في القائمة
1. **تحقق من القائمة الحالية** من المصدر الرسمي `alahlyegypt.com/ar` أو Wikipedia antes إنشاء/تعديل أي ملف لاعب.
2. لا تعتمد على ذاكرة قديمة — لاعبين يخرجون/يدخلون كل فترة.
3. المستخدم هو المصدر النهائي لأي شكوك في القائمة.

### بعد كل ماتش
1. **بعد صافرة النهاية مباشرة:** سجل voice note قصير عربي فقط بدل الكتابة. المحتوى: النتيجة، أبرز لحظات، أداء الملاعبة، تعليق المستخدم.
2. **بعد التسجيل:** حدّث `Matches/Log.md` + `Matches/Schedule.md`
3. حدث ترتيب الدوري في `Competitions/Premier-League.md`
4. حدث `Progress.md` عند الحاجة
5. حدث `Overview.md` و `Dashboard.md` فقط إذا تغير الرقم الرئيسي
6. سجل الإصابات/الإنذارات الجديدة في `Injuries.md`

### توليد الماتش
- الماتشات الودية والاستعراضية: لا تسجلها ولا تعمل voice note

### إضافة لاعب جديد
1. تحقق من وجوده في الفريق أولًا (راجع القائمة الرسمية).
2. أنشئ `Players/<player-name>.md`
3. استخدم نفس frontmatter: `name, number, position, season-rating, matches-played, goals, assists, yellow-cards, last-match-rating, image`
4. أضفه في `Squad.md` حسب المركز
5. أضف صورة رمزية في `Assets/Players/<english-slug>.jpg/png` إن وجدت

### إضافة مدرب/عضو جهاز
1. تحقق من Appointment رسمي قبل الكتابة.
2. حدث `Staff.md`
3. لصورة المدرب/الجهاز: `Assets/Staff/<english-slug>.jpg`

## صور وتسجيلات هوية
- **لا تفترض هوية صورة من وصفك alone** — اسأل المستخدم إذا لم تكن متأكدًا.
- عند تعدد الصور، استخدم ترقيم واضح `الصورة الأولى/التانية/التالتة` واطلب تأكيد.
- لا تنقل صورًا للمسار الخطأ بلا تأكيد — الصورة الخاطئة تخلّط القائمة.
- إذا توفرت صور رسمية من المستخدم، استخدمها مباشرة ولا تحمّل بدائل من الإنترنت除非 طلب صريح.

## naming convention
- مباريات: `YYYY-MM-DD - المسابقة vs الخصم.md`
- لاعبين: `Players/<player-name>.md`
- صور اللاعبين: `Assets/Players/<english-slug>.png`
- صور الجهاز: `Assets/Staff/<english-slug>.jpg`

## الإصابات والإنذارات
- كل حالة جديدة تُسجل في `Injuries.md`
- إذا بلغ لاعب 2 إنذار، لاحظه كـ `قريب من توقيف`
- الإصابات لها `from` و `until` إن أمكن

## Dataview queries المقترحة
```dataview
TABLE opponent, result, competition, date
FROM "01-Projects/Al-Ahly/Matches"
WHERE status = "played"
SORT date DESC
LIMIT 5
```

```dataview
TABLE name, season_rating, goals, assists, yellow_cards
FROM "01-Projects/Al-Ahly/Players"
SORT season_rating DESC
```

## Templater
- Template path: `/Hafsa/01-Projects/Al-Ahly/.obsidian/templates/Al-Ahly-Match.md`
- Smart fields: `season_progress`, `coach`, `man_of_the_match`, `attendance`, `weather`

## Assets والصور
- اللوجو canonical: `Assets/Al-Ahly-Logo.jpg`
- اللوجو SVG بديل: `Assets/Al-Ahly-Logo.svg`
- **لا تحمل صور رسمية من مواقع بدون إذن** — نستخدم placeholders/صور يقدمها المستخدم
- كل صورة تُشار إليها بـ `image:` في frontmatter

## Cron
- Job: `Hafsa Vault Index Sync Al-Ahly`
- الغرض: يتأكد أن `Overview.md` و `Index.md` محدّثين بعد التغييرات

## مصادر بيانات معتمدة
- Primary: https://www.alahlyegypt.com/ar
- Secondary: Wikipedia
- Tertiary: https://www.kooora.com + https://www.yallakora.com

### ملاحظات تشغيلية
- الموقع الرسمي `/ar/players` قد يعيد 404 — استخدم Wikipedia `2025–26 Al-Ahly SC season` كمسار بديل موثوق للقائمة الحالية.
- عند تغييرات كبيرة في القائمة: أنشئ ملفات jogadores/jquery الجدد بنظام YAML موحد بدل تعديل الملفات القديمة المفصلة.

## Cron
- Job: `Hafsa Vault Index Sync Al-Ahly`
- الغرض: يتأكد أن `Overview.md` و `Index.md` محدّثين بعد التغييرات
- ملاحظة: إذا تكرر الجوب أكثر من مرة في اليوم لنفس الملفات، ادمجه في جوب ليلي واحد خارج أوقات الذروة.
- لا تحذف أي بيانات قديمة بدون نسخ Archive أولاً
- ممنوع اختراق مواقع محمية بشكل مباشر — استخدم fetch/browser فقط
- كل تعديل يجب أن يُسجل في الملف المصدر ولا تعيد كتابة كل الملف إلا إذا طلب المستخدم
- لا ت脚踏ب صور/لوجوهات رسمية من الإنترنت بدون إذن صريح