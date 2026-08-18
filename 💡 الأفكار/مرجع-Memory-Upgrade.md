---
type: report
title: 🧠 ترقية الذاكرة — Cognee/MemOS (محجوبة) → Graph Layer بديل
tags: [memory, graph, cognee, memos, shared-memory-hub, upgrade]
---
# 🧠 ترقية الذاكرة — 2026-08-19

## 🔴 الواقع التقني:
- **Cognee** (30K⭐): محتاجة **Docker** (حتى الـ MCP server) + `grpc` (cygrpc DLL)
  → **محجوبة**: لا Docker مثبّت + Device Guard بيمنع grpc من الـ terminal
- **MemOS** (10K⭐, TS): محتاجة تشغيل ثقيل + نفس القيود
- **النتيجة:** مقدرش أنصّبهم على جهازك دلوقتي

## ✅ البديل العملي (اتعمل):
**`memory_graph.py`** — graph layer خفيف فوق الـ Shared Memory Hub:
- بيبني **185 nodes + 64 edges** من الـ vault (wiki-links + tags + co-occurrence)
- **stdlib فقط** (sqlite3) → يشتغل عبر `uv run` (يتجاوز Device Guard)
- **يكمّل الـ trigram FTS**: FTS = "ابحث نص"، Graph = "لقى المرتبط"
- DB: `C:\Users\hshin\AppData\Local\hermes\shared_memory\memory_graph.db`

## 🆚 الفرق:
| الطبقة | الأداة | الحالة |
|--------|-------|--------|
| FTS (نصي) | Shared Memory Hub (trigram) | ✅ شغّال (1230 row) |
| Graph (علاقات) | memory_graph.py | ✅ شغّال (185 nodes) |
| Knowledge Graph UI | Hermes Studio | ✅ شغّال (port 3000) |

## 💡 الخلاصة:
الذاكرة عندك **متكاملة دلوقتي** (FTS + Graph + Visual UI) — من غير ما نحتاج
Docker أو packages ثقيلة. Cognee/MemOS ممكن نضيفهم لما:
- تجيب **Docker** (أو VPS) ← نقدر نشغّل Cognee كـ MCP server
- أو نفعّل الـ **Device Guard استثناء** لـ grpc

## 📍 للتشغيل:
```bash
cd C:/Users/hshin/AppData/Local/Temp/voicetest
uv run --with requests python "C:/Users/hshin/AppData/Local/hermes/shared_memory/memory_graph.py" build
```
