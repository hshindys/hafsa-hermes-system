---
type: architecture
title: 🏗️ HARNESS.md — بنية نظام هفصة (الحزام الوكيلي)
tags: [harness, architecture, agent, context, tools, verification, guardrails]
---
# 🏗️ HARNESS.md — بنية نظام هفصة (Agent Harness)

> مستوحى من فيديو "Agent Harness / هندسة الحزام" (2026).
> الفكرة: النموذج = عقل قابل للاستبدال؛ الـ harness = البنية التحتية الثابتة.
> أي ترقية نموذج ترث كل إمكانيات الـ harness فوراً.

## 🔧 الـ 4 محاور الأساسية (مكتملة في نظامنا):

### 1. Tool Integration (تكامل الأدوات) ✅
- **Terminal**: Hermes يشغّل أوامر حقيقية (bash) + background processes
- **File System**: قراءة/كتابة/تعديل ملفات الـ vault
- **Browser**: `browser_exec` (real browser via Browser Use)
- **External APIs**: Zapier MCP (9000+ app)، NVIDIA NIM، Notion، OpenRouter
- **Git**: vault backup → GitHub (`hafsa-hermes-system`)

### 2. Context & Memory Management ✅
- **Shared Memory Hub**: trigram FTS (1230 row) + Arabic search
- **memory_graph.py**: graph layer (185 nodes) — علاقات بين الملفات
- **Hermes Studio**: Knowledge Graph visual (port 3000)
- **Notion**: second brain mirror (hourly sync)
- **Context injection**: الـ agents بيقرأوا الـ MEMORY.md + USER.md أوتوماتيك

### 3. Agentic Loop (الحلقة التكرارية) ✅
```
Grill Me (اسأل قبل) → Vibe Coding (خطّط) → Dark Factory (نفّذ)
   → Observe outputs → Adapt → Repeat → Deliver
```
- **Grill Me**: pre-alignment interview (يمنع الـ blind start)
- **Vibe Coding Rules**: خطّط ← اتبع patterns ← review ← قلّل slop
- **Dark Factory**: بيشغّل coding agents في loop منظّم

### 4. Verification & Guardrails ✅
- **pruning_checker.py**: يشيل الـ no-op skills
- **skill_security_scan.py**: فحص أمان (curl|bash، leaks) — cron يومي
- **agent_trace.py**: append-only log لكل interaction (شفافية)
- **Hermes config**: tts provider + model routing محمي

## 🔄 Model Agnostic (النموذج قابل للاستبدال):
- **OpenClaw**: `nvidia-nim/z-ai/glm-5.2` + fallback (minimax-m3, deepseek-v4)
- **Hermes**: multi-provider (NVIDIA NIM، OpenRouter، إلخ)
- ترقية النموذج = يرث الـ context + الأدوات + الـ guardrails فوراً

## 📌 مبدأ هندسة الحزام (Harness Engineering):
> "أي نموذج قديم داخل harness يتفوّق على أحدث نموذج مجرّد"
> التركيز: تحسين **البيئة** مش تحسين الـ prompt

## 🔗 الملفات المرتبطة:
- `vibe_coding_rules.md` (قواعد الـ loop)
- `factory_rules.md` (قواعد Dark Factory)
- `مرجع-OpenClaw-Hardening.md` (model pinning)
- `shared_memory/` (Hub + graph + trace + security)

## 🎯 الخطوة الجاية:
- تقوية Verification Layer في Dark Factory (auto-verify قبل التسليم)
- ربط memory_graph بـ context injection أوتوماتيك
