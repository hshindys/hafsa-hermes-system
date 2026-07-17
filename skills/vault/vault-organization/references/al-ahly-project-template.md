# Al-Ahly Project Template
# مسار: /01-Projects/Al-Ahly/

## Overview.md
تستخدم Dataview لجلب آخر مباراة + القادمة.

## Match Log Schema
| التاريخ | الخصم | النتيجة | المسابقة | الهدف/الحالات |
|---|---|---|---|---|
| YYYY-MM-DD | opponent | W/L/D | league | notes |

## Schedule Schema
| التاريخ | الخصم | مسابقة | التوقيت (القاهرة) | الملعب | الحالة |
|---|---|---|---|---|---|
| YYYY-MM-DD | opponent | comp | HH:MM | stadium | upcoming |

## Competition File Schema
```md
---
tags: [al-ahly, football, premier-league|caf|cup]
---
# 🏆 <اسم المسابقة>
> المصدر: https://www.alahlyegypt.com/ar
> آخر تحديث: YYYY-MM-DD

## ترتيب المسابقة
// جدول الترتيب هنا

## مباريات الأهلي
// جدول المباريات هنا
```

## Squad Schema
```md
---
tags: [al-ahly, football, squad]
---
# 👥 تشكيلة الأهلي
> المصدر: https://www.alahlyegypt.com/ar

## المدير الفني
- **الاسم:** ...
- **الجهاز:** ...

## حراس المرمى / مدافعون / وسط / هجوم
| # | الاسم | الرقم | إصابات/إنذارات |
|---|---|---|---|
```

## News Schema
```md
---
tags: [al-ahly, football, news] 
---
# 🔗 مصادر وأخبار الأهلي
## مصادر رسمية
- ...

## ملخصات وفيديوهات
| التاريخ | الوصف | الرابط |
|---|---|---|
```

## Frontmatter Standard
```yaml
---
type: note
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [al-ahly, football, egypt, premier-league|caf|cup]
status: active
source: https://www.alahlyegypt.com/ar
---
```
