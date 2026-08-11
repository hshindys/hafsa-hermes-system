---
type: reference
title: تنصيب Buzz + ربطه بـ Hermes (مرجع مستقبلي)
tags: [buzz, hermes, vps, فريق, خصوصية, مرجع]
---
# 🐝 تنصيب Buzz + ربطه بـ Hermes (مرجع لوقت لاحق)

> **الحالة:** مؤجّل — محتاج VPS (الفيديو استخدم Hostinger KVM2). إنته حالياً على
> Discord + Telegram. ده مرجع يتفعّل لما تتوفر VPS.

## المتطلبات
- Hermes **v0.20+** ✅ (عندك v0.20.0 مثبّت)
- VPS (الفيديو: Hostinger **KVM2** = 2 CPU / 8GB RAM — تجنّب KVM1 لو عايز التطبيقين)
- حساب Buzz (buzzbuzz.xyz) + **public key (hex)** من الملف الشخصي

## الخطوات (من الفيديو TQoSP71iXWY)
1. اشترِ VPS (KVM2)، طبّق كوبون `HermES` (10% لأول مرة).
2. من لوحة Hostinger → **one-click deploy** → اختَر **Buzz** → Deploy.
3. استرجع الـ **public key** من ملفك الشخصي في Buzz (الصيغة **hexadecimal** — مش mpub).
4. الصق الـ key في إعداد Buzz واضغط Deploy (بيتنصّب على الـ VPS بتاعك).
5. في Hermes: update لـ 0.20 → افتح gateway config → اختر قناة `buzz` →
   أدخل URL المجتمع → اترك الـ private key فاضي → Enter.
6. اختبر: ابعت prompt لـ Hermes من داخل Buzz وشوف الرد.

## المميزات
- بيانات الفريق محفوظة على الـ VPS بتاعك (خصوصية أعلى من Slack).
- تقدر تضيف وكلاء متعددين (Hermes/Claude/OpenAI) كزملاء في قناة واحدة.
- تعمل cron jobs من داخل Buzz.

## ملاحظة
- Buzz **مش مدمج** في كود Hermes عندك حالياً (0.20.0 / 2026.8.3) — الفيديو بيقول
  اتضاف "امبارح". لو ظهرت نسخة أحدث فيها buzz، شغّل `hermes update` وأعد المحاولة.
- بديل مؤقت: استخدم NVIDIA NIM (اللي ضفناه) ضد tencent/hy3 لعمل "منافسة نماذج"
  من غير Buzz.
