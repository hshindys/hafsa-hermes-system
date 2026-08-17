---
type: dashboard
title: 📊 لوحة القيادة (Dataview)
tags: [dashboard, dataview, قيادة, مهام, تقارير]
---
# 📊 لوحة القيادة — Hafsa OS

> لوحة مرئية للـ vault باستخدام **Dataview** (plugin في Obsidian).
> 📥 تثبيت: Settings → Community plugins → Browse → ابحث "Dataview" → Install → Enable

## 📋 المهام من لوحة الكانبان
```dataview
TABLE status AS "الحالة", priority AS "أولوية"
FROM "🎯 المشاريع"
WHERE file.name = "لوحة-المهام-كانبان"
```

## 💊 خطة الأدوية (اليوم)
```dataview
LIST
FROM "💊 طبي"
WHERE file.name = "الخطة-اليومية-المتكاملة-مخصصة"
```

## 📅 آخر اليوميات
```dataview
TABLE file.mtime AS "آخر تحديث"
FROM "📅 اليوميات"
SORT file.mtime DESC
LIMIT 7
```

## 💡 أحدث الأفكار
```dataview
TABLE file.mtime AS "وقت"
FROM "💡 الأفكار"
SORT file.mtime DESC
LIMIT 10
```

## 🔧 حالة النظام (من المراقبة)
```dataview
LIST
FROM "💡 الأفكار"
WHERE file.name = "مراقبة-النظام-2026-08-15"
```

---
_لوحة حية — تتحدّث أوتوماتيك مع Dataview كل ما فتحت Obsidian._
