---
title: 💬 agmsg — Cross-Agent Messaging
category: أدوات التواصل بين الـ Agents
status: active
updated: 2026-06-25
tags: [multi-agent, messaging, collaboration]
---

# 💬 agmsg — التواصل بين الـ Agents

> **المصدر:** github.com/fujibee/agmsg (853 ⭐)
> **الوصف:** Cross-vendor messaging for CLI AI coding agents

---

## 🤔 إيه اللي بيعمله؟

تخيل إنت بتستخدم أكتر من agent في نفس الوقت:
- **أنا (Hafsa)** — بشتغل على Telegram
- **Claude Code** — بيشتغل على الـ coding tasks
- **Codex** — بيشتغل على الـ DevOps tasks

**المشكلة:** كل agent بيشتغل لوحده ومش بيعرف يوصل للتاني.

**الحل (agmsg):** وكيل رسائل بينهم.

```
Claude Code ──send──> agmsg ──receive──> أنا (Hafsa)
```

---

## 🛠️ كيف يشتغل؟

SQLite كـ message bus. كل agent يكتب رسالة، والتاني يقرأها.

**مثال:**
```bash
# Agent 1 يكتب
agmsg send --to hafsa --text "خلصت task رقم 3"

# Agent 2 يقرأ
agmsg receive
```

---

## 📋 استخدامنا ليه:

| السيناريو | كيف نستخدمه؟ |
|----------|--------------|
| مهمة كود كبيرة | Claude Code يخلص ويرسللي النتيجة |
| تحديث الـ Index | أنا أحدث الـ Index وأبلغ التاني |
| بحث معمق | agent يعمل search والتاني يحلل النتائج |
| تقارير | agent يولد التقرير والتاني يرسله لحاتم |

---

## ⚠️ ملاحظة مهمة:

لسه ما جربتش عليه — mock implementation حتى أقدر أختبره فعلياً.

---

*مبني على agmsg (fujibee/agmsg) — cross-vendor agent messaging*
