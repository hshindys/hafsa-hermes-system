---
type: setup
title: 🔧 OpenClaw Omnirouter Hardening (2026-08-19)
tags: [openclaw, omnirouter, hardening, nvidia-nim, fix, 401, 429]
---
# 🔧 OpenClaw Omnirouter Hardening — 2026-08-19

## ✅ الإصلاح المتعلق بالـ 401/429
المشكلة: OpenClaw كان مثبّت على `auto/*` combos (omniroute-remote) اللي بتموت
وترجّع 401/429 متكرر.

**الحل المطبّق:**
- `agents.defaults.model.primary` ← `nvidia-nim/z-ai/glm-5.2` (مباشر، مش combo)
- `agents.defaults.model.fallbacks` ← `["nvidia-nim/minimaxai/minimax-m3", "nvidia-nim/deepseek-ai/deepseek-v4-flash-0731"]`
- شيلنا الـ `auto/*` combos الميتة من الـ fallbacks
- الـ `nvidia-nim` provider متظبط بـ `baseUrl: https://integrate.api.nvidia.com/v1` + `apiKey: NVIDIA_API_KEY` (من env)

**أعيد تشغيل الـ gateway:**
- قُتل PID 16900، شُغّل تاني (PID 15468) على port 18789 ✅
- Omnirouter شغّال على 20128 ✅

## ⚠️ ملاحظة مهمة:
- Omnirouter (20128) **مش متظبط بـ nvidia-nim** (بيقول "No active credentials").
- لكن OpenClaw بيستخدم `nvidia-nim` provider **مباشرة** (مش عبر Omnirouter) ← ده الصح.
- لو حبيت تستخدم Omnirouter كـ proxy، لازم تسجّل `nvidia-nim` في DB بتاعه
  (`~/.omniroute/storage.sqlite` → `provider_connections`).

## 📍 للتشغيل المستقبلي:
```bash
# شغّل Omnirouter
# (عبر ~/.openclaw/omniroute.cmd)

# شغّل OpenClaw gateway
node "C:/Users/hshin/AppData/Roaming/npm/node_modules/openclaw/dist/index.js" gateway --port 18789
```

## 🔗 المرجع:
- `skills/productivity/openclaw-omnirouter-troubleshooting/` (SKILL.md + scripts)
- `scripts/pin_sessions_to_nim.py` (repin sessions to NVIDIA)
- `scripts/openclaw_nim_watchdog.py` (monitor key health)

## ✅ الحالة: مصلّح (pin مباشر على NVIDIA، fallback chain جاهز)
