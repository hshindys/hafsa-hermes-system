---
type: reference
title: OpenCode محلي + NVIDIA NIM (واجهة برمجة آمنة)
tags: [opencode, nvidia, nim, coding-agent, واجهة, آمن]
---
# 🖥️ OpenCode محلي + NVIDIA NIM

> بديل آمن لـ t3.codes (الفيديو `om7-t-Kg8Ew`). كله على جهازك، المفاتيح من `.env` مش منصة تالتة.

## الإعداد
- **OpenCode:** منزّل عندك (`opencode-ai@1.18.18`)
- **الكونفيج:** `C:\Users\hshin\AppData\Roaming\opencode\opencode.json`
  - provider `nvidia` → baseURL `https://integrate.api.nvidia.com/v1`
  - models: `z-ai/glm-5.2`, `moonshotai/kimi-k2.6`, `minimaxai/minimax-m3`, `deepseek-ai/deepseek-v4-flash-0731`
  - provider `tencent` (custom openai-compatible) → OpenRouter `tencent/hy3:free`

## التشغيل (آمن — المفتاح من .env)
شغّل:
```
C:\Users\hshin\AppData\Local\hermes\opencode-nvidia.bat
```
الـ `.bat` بيقرأ `NVIDIA_API_KEY` من `.env` ويحطه في env قبل ما يشغّل opencode — **المفتاح مش متخزّن في الكونفيج**.

## لو عايز تضيف المفتاح يدوياً
داخل OpenCode نفّذ: `/connect` واختار NVIDIA، حط المفتاح (بيتخزّن في `~/.local/share/opencode/auth.json`).

## اختيار الموديل
داخل OpenCode: `/models` واختار `z-ai/glm-5.2` (أو غيره من NVIDIA).

## مميزات زي t3.codes (وحلو أكثر)
- GUI بديل للـ terminal
- push/pull على GitHub/GitLab
- commit message generation تلقائي
- كل agent على branch لوحده

## ⚠️ أمان
- بلاش تحط مفاتيحك على منصة تالتة (زي t3.codes) — OpenCode محلي = أمان 100%.
- المفاتيح اللي اتشاركت في الشات (nvapi-*) لسه لازم تتلغى.
