---
type: mission
title: Mission — مهمة المصنع الآلي (Dark Factory)
tags: [mission, dark-factory, أهداف, نطاق, prd]
---
# 🎯 Mission — مهمة المصنع الآلي

> مشتق من PRD حاتم. يحدد **الأهداف** و **خارج النطاق** عشان الـ agent يقرر يقبل أو يرفض أي spec جديد.

## 🟢 الأهداف (In Scope)
1. **أتمتة إدارة المعرفة الصحية لحاتم:**
   - خطة طبية مخصصة (109kg → 95-100kg) + متابعة أسبوعية + تفاصيل تمرين.
   - تذكير أدوية (صباح 05:00 / مساء 22:30) عبر Telegram/Discord.
2. **Shared Memory Hub:** ذاكرة موزعة (ملفات + قواعد + ملاحظات) بـ trigram FTS للعربي.
3. **أدوات برمجة محلية مجانية:** OpenCode + NVIDIA NIM (glm/kimi/mini/dsv4) + worktree isolation.
4. **فريق Bots:** researcher (بحث) + reportwriter (تقارير) + دلع (رسائل صوتية سخنة).
5. **مراقبة النظام:** SystemHealthCheck يومياً 08:00 + تقرير لـ Telegram.
6. **باك أب GitHub:** vault على `hafsa-hermes-system` (branch vault-backup).
7. **self-hosted (عند توفر VPS):** Immich / RustDesk / AppFlowy / Buzz.

## 🔴 خارج النطاق (Out of Scope) — يُرفض تلقائياً
1. ❌ **أي اشتراك مدفوع** (Claude Pro / Codex / Grok Bot) — إنته على NVIDIA/tencent المجانيين.
2. ❌ **أدوات مغلقة المصدر** تتطلب work email أو macOS فقط (Xirp, GrokBot, Open Mousebot حالياً).
3. ❌ **مشاركة مفاتيح حقيقية** في الشات العام أو ملفات متتبعة بـ git.
4. ❌ **نشر كود قبل المراجعة** (Validator لم يمرره).
5. ❌ **محتوى طبي تشخيصي** — Hermes يذكّر بالأدوية فقط، لا يشخّص.
6. ❌ **أي شيء يخص حساسية حاتم الغذائية** (مأكولات بحرية) — محظور تماماً.
7. ❌ **تعديل `config.yaml` يدوياً** — فقط عبر `hermes config set`.

## 📋 معايير قبول Spec جديد
- يخدم هدفاً من In Scope ✅
- لا يتطلب أداة مدفوعة أو مغلقة ❌
- يحترم أمان المفاتيح والقيود الطبية ✅
- قابل للتقسيم لخطوات صغيرة (bite-size) ✅

## 🚨 آلية الرفض
الـ agent له الحق يرفض spec يقول: "ده خارج النطاق (انظر mission.md §Out of Scope)".
مثال: spec "اشترك في GrokBot بـ $300" → **مرفوض** (هدف 2 في Out of Scope + مدفوع).
