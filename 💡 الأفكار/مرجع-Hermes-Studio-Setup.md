---
type: setup
title: 🖥️ Hermes Studio — لوحة التحكم الموحّدة (Setup 2026-08-19)
tags: [hermes-studio, dashboard, web-ui, setup, multi-agent, cron-ui]
---
# 🖥️ Hermes Studio — لوحة التحكم الموحّدة

> Setup notes لـ Hermes Studio (web UI للـ Hermes Agent) — اتثبّت وشغّال.

## ✅ الحالة: شغّال
- **Hermes Studio**: `http://127.0.0.1:3000` (LISTENING)
- **Hermes serve (backend)**: `http://127.0.0.1:9119` (شغّال في background)
- **Studio متصل بـ Hermes serve** ✅ (الـ log بيقول "using external API: 9119")

## 📍 المسارات
- Repo: `C:\Users\hshin\AppData\Local\hermes\tools\Hermes-Studio`
- `.env`: `HERMES_API_URL=http://127.0.0.1:9119`
- Backend: `hermes serve --port 9119 --host 127.0.0.1` (background PID)

## 🚀 تشغيل (لما تعيد فتح)
```bash
# 1. شغّل الـ backend
cd C:\Users\hshin\AppData\Local\hermes
hermes serve --port 9119 --host 127.0.0.1 &

# 2. شغّل الـ Studio
cd C:\Users\hshin\AppData\Local\hermes\tools\Hermes-Studio
cmd /c "set NODE_OPTIONS=--max-old-space-size=2048 && node_modules\.bin\vite --port 3000 --host 127.0.0.1"
```
افتح: `http://127.0.0.1:3000`

## ✨ المميزات اللي بتفيدك (موجودة في Studio):
- 🕸️ **Knowledge Graph** — خريطة الذاكرة مرئية (يكمّل Shared Memory Hub)
- 📋 **Kanban Board** — بديل الـ kanban اليدوي (Backlog→Todo→In Progress→Review→Done)
- ⏰ **Cron Manager** — الـ 18 job بتوعك ظاهرين في UI (create/edit/pause/trigger)
- 🤖 **Multi-Agent Crews** — يزامن الـ bots (researcher/reportwriter) + worktree
- 🔐 **Execution Approvals** + **Audit Trail**
- 🖥️ **System Health Panel** — يكمّل `system_health_monitor.py`
- 🪪 **Identity Editor** — يعدّل SOUL.md/persona من المتصفح

## ⚠️ ملاحظات:
- Studio مبني لـ Hermes v0.9.0 — إنته عندك v0.20.1 (أحدث). معظم المميزات شغّالة، بس ممكن اختلافات طفيفة في API.
- Redis اختياري (فيه fallback لـ file storage).
- عشان تفتحه من الموبايل: استخدم Tailscale (زي ما الـ README بيقول).

## 🔗 المصدر:
- https://github.com/JPeetz/Hermes-Studio
