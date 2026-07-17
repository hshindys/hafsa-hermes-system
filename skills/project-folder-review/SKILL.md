---
name: project-folder-review
description: >
  MUST USE when reviewing a project folder for broken links, missing assets,
  outdated references, or TODO/FIXME items. Produces a prioritized fix list.
  NOT for: general file search, full vault reindex, destructive edits.
---

# Project Folder Review — دليل الاستخدام

## متى نستخدمه
- فحص مشروع جديد/قديم قبل التسليم
- اكتشاف روابط مكسورة أو ملفات مفقودة
- لائحة مهام إصلاح مرتبة بالأولوية

## كيف تشغله
1. اختر المجلد المستهدف.
2. افحص:
   - ملفات HTML/MD فيه روابط داخلية 🔗
   - ملفات الصور/الفيديو المذكورة في المحتوى 🖼️
   - ملفات الكود المسماة لكن غير موجودة 🐍
   - تعليقات TODO/FIXME/BROKEN في الكود 📝
3. صنّف النتائج:
   - **حرج** — يوقف العمل الآن
   - **هام** — يُصلح خلال 24 ساعة
   - **تحسين** — لاحقاً
4. أرسل لائحة مختصرة + اقتراح أمر إصلاح لكل بند.

## قواعد مهمة
- لا تحذف/تعدل ملفات قبل موافقة
- لا تذكر مسارات حساسة أو بيانات شخصية
- ركز على items واحدة قابلة للتنفيذ لكل recommendation
