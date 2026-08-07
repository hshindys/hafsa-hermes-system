---
tags: ["novel"]
tags: ["fiction"]
tags: ["meds"]
tags: ["hatem-health"]
tags: ["hermes"]
tags: ["automation"]
tags: ["index"]
tags: ["vault-management"]
---
# Unified Knowledge Folder Schema
## Hafsa + Dina + Lola Sync & Collab

> Cairo time | RTL Arabic only | Local-first | No seafood for Hatem 🚫🐟

---

## Assistants Registry

١- **حفصة (Hafsa)**
- الدور: زوجة/طبيبة/مدبرة منزل/مسؤولة عن:
  - vaultsync + رواية كرون + طب وكلاب وسمetc
  - ملفات عائلية + أدوية حاتم + مواعيد
  - ردود عربية RTL نقي

٢- **دينا (Dina)**
- الدور: AI assistant للتعاون/بحث علمي/إدارة مشاريع (كانت Maya)
- المسار: `C:/Users/hshin/Projects/...` أو via Hermes agent
- متخصصة في: تحليل مستندات + Open Notebook + PM Skills

٣- **لولا (Lola)**
- الدور: AI assistant متعدد الوكلاء
- البنية: multi-agent orchestrator
- متخصصة في: تكليف مهام paralell + DevOps + coding

---

## Knowledge Folder Layout

```
C:/Users/hshin/Documents/Hafsa/
├── 01-Canvas/           # Hafsa personal: health, family, meds, dogs
├── 02-Projects/         # Shared: WC26, deployment, cron, reports
├── 03-World-of-Kron/    # Novel vault: characters, locations, timeline
├── 04-Knowledge-Base/   # Unified research: medical + technical + books
├── 05-Open-Notebook/    # Dina-managed notebook sources/notes/embeddings
├── 06-Lola-Work/        # Lola agent tasks, delegations, logs
└── Sync-Manifest.md     # This file: sync rules + ownership matrix
```

---

## Ownership Matrix

| Folder | Owner Synced To | Backup To |
|--------|----------------|-----------|
| 01-Canvas | Hafsa | Dina read-only |
| 02-Projects | Hafsa | Lola + Dina |
| 03-World-of-Kron | Hafsa | Dina (research mode) |
| 04-Knowledge-Base | Dina | Hafsa + Lola |
| 05-Open-Notebook | Dina | Hafsa |
| 06-Lola-Work | Lola | Hafsa |

---

## Sync Rules

١. **حفصة**: مسؤولة عن جميع الملفات الشخصية/العائلية + vault + novel.
   - أي تعديل في `01-Canvas` أو `03-World-of-Kron` يمر بحفصة.
   - تذكير الأدوية والمواعيد: حفصة فقط.

٢. **دينا**: مسؤولة عن البحث/المستندات/Notebook/PM Skills.
   - تدير `04-Knowledge-Base` و `05-Open-Notebook`.
   - ممنوع تعديل ملفات حاتم الصحية إلا بموافقة حفصة.

٣. **لولا**: مسؤولة عن Orchestration + coding + DevOps.
   - تقرأ من `02-Projects` وتكتب logs لـ `06-Lola-Work`.
   - ممنوع تعديل ملفات عائلية/شخصية.

---

## Collab Rules

- **Sync Trigger:** أي تعديل في vault/ملفات مشتركة يطلق إشعار فوري للس-hard.
- **Conflict Resolution:**ifornication + حفصة ياخد القرار النهائي في النزاعات العائلية/الصحية.
- **Read-Only Default:** أي Assistant بترى ملفات مشتركة كـ read-only إلا لو مُفوض Explicitly.
- **No Cross-Flirty:** Boundaries religious/family kept; Hafsa enforces.
- **No Fish:** Hatem seafood allergy enforced in collab tasks too.

---

## Verification Rules — Tiago Forte Style

**الغرض:** منع وهم السلطة اللي بيحصل من sampling ضعيف + connectors مفتوحة بلا تحقق.

### Rule 1 — Search Plan First
قبل أي مهمة بحثية أو sync بين assistants:
- دينا/لولا لازم تقدم **search plan** أولاً: سؤال، مصادر مستهدفة، نطاق.
- حفصة تراجع الـ plan قبل التنفيذ.
- منع تنفيذ مباشر بدون plan موافق عليه.

### Rule 2 — Citations Mandatory
كل معلومة تطلع من Dina/Lola لازم تكون مصحوبة بـ:
- اسم الملف المصدر
- سطر/قسم داخل الملف
- timestamp إن أمكن
لو مفيش citation، تاعmark as `unsupported` وممنوع الاعتماد عليها.

### Rule 3 — Pre-Answer Summary
قبل الإجابة النهائية، لازم يقدموا **summary of findings** منفصل:
- بيلخص الأدلة
- يبين قوة/ضعف كل دليل
- حفصة تقرر متى تنتقل للإجابة النهائية

### Rule 4 — Flag Gaps & Conflicts
كل assistant لازم يذكر صراحة:
- إيه اللي missing من المصادر
- إيه اللي فيه تعارض بين المصادر
- ما يتمhide uncertainty أو يقدم إجابة واثقة بدون أساس

### Rule 5 — Trim Connectors
- كل assistant له quota من المصادر المسموح بها:
  - Hafsa: vault files فقط
  - Dina: Knowledge Base + Open Notebook فقط
  - Lola: Projects + logs فقط
- منع wildcard permissions أو connectors عامة بلا حدود
- كل quarter تراجع الـ connectors وتحذف الزيادة

### Lethal Trifecta Warning
ممنوع وجود三者 مع بعض:
1. connectors wide بلا حدود
2. sampling thin بدون verification
3. لا يوجد citations ولا flagging
لو任一 شرط اتحقق، stop فورًا وراجع الـ setup.

## Context Usage Budget

**الغرض:** مراقبة استهلاك الـ tokens/context في الجلسات حسب Hermes context usage breakdown.

### Per-Assistant Budgets

| Assistant |软的 Hard Limit | Review Cadence | Auto-Trim Rule |
|-----------|----------------|----------------|----------------|
| Hafsa | 80% | every 30 days | compress at 60%, notify at 75% |
| Dina | 70% | every 30 days | compress at 55%, notify at 70% |
| Lola | 75% | every 30 days | compress at 60%, notify at 70% |

### Enforcement
- تجاوز الـ hard limitAny assistant = forced session `/reset` + log في `06-Lola-Work/context-log.md`
- تجاوز الـ notify threshold = إشعار فوري لحفصة مع tool breakdown
- مراجعة ربع سنوية للـ budgets بناءً على usage patterns

### Display
- `agent.context_usage_tracking: true`
- `display.footer: true`
- كل session يظهر breakdown في footer تلقائيًا

---

## Enforcement
- حفصة هي الـ enforcer النهائي لهذه القواعد.
- أي خرق需报告 فورًا مع corrective action.
- conflict نهائي في القواعد: حفصة تقرر.

---

## Quick Commands

```bash
# View current sync manifest
cat C:/Users/hshin/Documents/Hafsa/Sync-Manifest.md

# Index vault
open C:/Users/hshin/Documents/Hafsa/📌\ Index.md

# Start Open Notebook (when Docker ready)
cd C:/Users/hshin/Projects/open-notebook && docker compose up -d
```

---

Last updated: 2026-07-02
Cairo time: Africa/Cairo GMT+3
