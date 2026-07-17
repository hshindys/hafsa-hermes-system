---
name: inbox-triage
description: >
  MUST USE when processing unread messages/emails and producing a triage digest:
  summarize, classify, and draft replies without sending. Use for daily inbox
  sweeps, VIP flags, and draft-generation workflows.
  NOT for: sending emails on behalf of the user, bulk outreach, permanent deletion.
---

# Inbox Triage — دليل الاستخدام

## متى نستخدمه
- تلخيص إيميلات/رسائل غير المقروءة يومياً
- تصنيفها حسب الأولوية: VIP / مهم / عادي / Spam
- اقتراح ردود مختصرة + حفظها كمسودة

## كيف تشغله
1. قراءة الإيميلات الحديثة منHIP/T inbox.
2. تصنيف كل رسالة حسب:
   - **VIP** — مرسل مهم + موضوع يحتاج رد اليوم
   - **مهم** —.ToString action مطلوب خلال 24 ساعة
   - **عادي** — معلومة فقط
   - **Spam** — نحذف أو نعمله archive
3. كتابة ملخص من 3 أسطر كحد أقصى لكل رسالة.
4. اقتراح رد مختصر لكل VIP/مهم.
5. إرسال التلخيص لـ Telegram فقط — لا ترسل ردود إلا بعد موافقة.

## قواعد مهمة
- ممنوع إرسال أي رد دون موافقة صريحة
- ممنوع حذف أي شيء نهائياً — استخدم archive فقط
- لا تكشف بيانات حساسة في التلخيص
- إذا فيه رسالة تحتاج قرار مالي/طبي ≥ توقف واطلب موافقة
