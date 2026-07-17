---
name: website-monitor
description: >
  MUST USE when monitoring a website/page for changes or outages and alerting on diffs.
  Produces a short status report + change summary when content changes.
  NOT for: full-text scraping audits, competitor analysis, bulk archive downloads.
---

# Website Monitor — دليل الاستخدام

## متى نستخدمه
- متابعة صفحة هامة (مثال: مباراة مصر، صفحة مشروع)
- تنبيه عند تغيير المحتوى أو حالة الموقع
- تقرير يومي/أسبوعي باختلافات بسيطة

## كيف تشغله
1. تحدد الهدف: URL + عدد الصفحات + selectors اختيارية
2. اجلب HTML الحالي وقيّسه hash/snippet.
3. قارنه بالنسخة السابقة إذا موجودة.
4. صنّف:
   - **تغيير** — أرسل ملخص التعديل
   - **لا يوجد تغيير** — لا ترسل أي شيء
5. خزن snapshot جديد للمقارنة القادمة.

## قواعد مهمة
- لا ترسل تنبيه إذا لا يوجد تغيير فعلي
- لا تحفظ محتوى حساس (كلمات سر/بيانات شخصية)
- عدد المرات: يومياً أو عند الطلب فقط
