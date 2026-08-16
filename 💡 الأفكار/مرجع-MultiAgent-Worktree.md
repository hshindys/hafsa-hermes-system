---
type: guide
title: Multi-Agent Worktree Setup (بديل Xirp مفتوح)
tags: [multi-agent, worktree, opencode, nvidia, telegram, orchestration, xirp-alternative]
---
# 🤖 Multi-Agent Worktree Setup — بديل Xirp المفتوح

> بديل لـ Spotify Xirp (الفيديو `8WppW2ImqMw`). Xirp **macOS-only + closed source + بي leaked transcripts** — ده البديل على Windows بتاعك.

## المميزات (زي Xirp بالظبط)
- ✅ **عزل تام:** كل agent في **git worktree** منفصل (branch `agent/<name>`) — مفيش collision
- ✅ **Hot-swap models:** NVIDIA NIM (GLM/Kimi/MiniMax/DeepSeek) عبر OpenCode
- ✅ **إشعار Telegram:** يبلغك على تليجرام لما agent يخلص (عبر Hermes)
- ✅ **مفتوح المصدر + على جهازك** (أمان 100%)

## الملفات
- `C:\Users\hshin\AppData\Local\hermes\shared_memory\multi_agent_worktree.py` — السكريبت
- `C:\Users\hshin\AppData\Local\hermes\opencode-nvidia.bat` — launcher بمفتاح من `.env`

## التشغيل
```bash
# شغّل agent جديد (ياخد الـ branch الحالي كـ base تلقائياً)
python multi_agent_worktree.py --name "agent-1" --model "z-ai/glm-5.2"

# agent تاني على نفس الـ repo (worktree منفصل)
python multi_agent_worktree.py --name "agent-2" --model "moonshotai/kimi-k2.6"

# تحديد base مختلف
python multi_agent_worktree.py --name "ui" --base master
```

كل أمر:
1. ينشئ worktree في `D:\vaults\_wt_<name>` على branch `agent/<name>`
2. يفتح OpenCode فيه (متصل بـ NVIDIA NIM)
3. يبعت إشعار Telegram لـ `779043832`

## تنظيف
لما تخلص:
```bash
cd D:\vaults\Hafsa
git worktree list
git worktree remove "_wt_<name>" --force
```
⚠️ لازم تقفل OpenCode بتاع الـ worktree الأول (`taskkill /f /im opencode.exe`) قبل الـ remove.

## ⚠️ أمان
- Xirp بيـleak transcripts — إحنا **مش** بنعمل ده (كل حاجة محلية).
- المفاتيح من `.env` مش في الكونفيج.
- Telegram ID محفوظ في السكريبت (`779043832`) — غيّره لو عايز.
