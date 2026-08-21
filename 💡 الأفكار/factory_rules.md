---
type: rules
title: 🏭 Dark Factory — قواعد المصنع المظلم (مع Verification Layer)
tags: [dark-factory, rules, verification, guardrails, agentic-loop, quality]
---
# 🏭 Dark Factory — قواعد المصنع المظلم

> مستوحى من فيديو "Agent Harness" — الـ Verification Layer أهم من النموذج نفسه.
> أي مهمة coding تعدّي من الـ pipeline ده قبل التسليم.

## 🔄 الـ Agentic Loop (مStructure):
```
1. GRILL (اسأل)    → Grill Me: وضّح المطلوب قبل تبدأ
2. PLAN (خطّط)     → Vibe Coding: اكتب PLAN (هدف + خطوات + ملفات)
3. BUILD (ابنِ)    → نفّذ الكود باprintf step-by-step
4. VERIFY (تحقّق)  → [LAYER إلزامي] شغّل tests + فحص no-ops + أمن
5. ADAPT (عدّل)    → لو فيه خطأ ← صلّح وكرّر من 3
6. DELIVER (سلّم)  → commit + report
```

## 🛡️ Verification Layer (إلزامي قبل DELIVER):
كل مهمة لازم تعدّي على:
1. **No-op check**: `pruning_checker.py` — أي سطر ماعملش حاجة؟ احذفه
2. **Security scan**: `skill_security_scan.py` — curl|bash؟ leaked secrets؟
3. **Trace log**: `agent_trace.py log` — سجّل الـ interaction (شفافية)
4. **Self-review**: الـ agent يقرأ الكود بتاعه قبل يسلّمه (error handling؟ null checks؟)
5. **Tests**: لو فيه test suite ← شغّله؛ لو لأ ← اكتب smoke test بسيط

## 🔒 Guardrails (حدود أمان صارمة):
- ممنوع `rm -rf /` أو delete كبير بدون تأكيد
- ممنوع hardcoded secrets (استخدم `.env` / Vault)
- ممنوع curl|bash من URLs مش موثوقة
- ممنوع تعديل `config.yaml` يدوياً (استخدم `hermes config set`)

## 📊 Observability:
- كل مهمة ← `agent_trace.py` (append-only log)
- يومياً ← `SkillSecurityScan` cron (4am) يفحص الـ skills
- `system_health_monitor.py` يراقب الموارد

## 🔗 العلاقة:
- **Grill Me**: الخطوة 1
- **vibe_coding_rules.md**: الخطوة 2 + 5
- **pruning_checker / skill_security_scan / agent_trace**: الخطوة 4
- **HARNESS.md**: البنية الكاملة

## 📌 تفعيل:
هذه القواعد تُقرأ في أي coding session. أي agent في Dark Factory يتبعها.
