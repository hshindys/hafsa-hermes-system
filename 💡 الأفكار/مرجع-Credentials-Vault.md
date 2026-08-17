---
type: reference
title: Credentials Vault Pattern (OpenCode + Hermes)
tags: [أمان, مفاتيح, credentials-vault, opencode, hermes, env]
---
# 🔐 Credentials Vault Pattern — OpenCode + Hermes

> نمط أمان مأخوذ من فكرة "Credentials Vault" في MindHub/Anton (الفيديو QID-QHVLYYc):
> **المفاتيح تُحمّل من بيئة محمية (.env) وقت التشغيل — مش متكتوبة في أي config أو كود.**

## 🎯 المبدأ
- ❌ **ممنوع:** مفتاح API في `opencode.json` أو `config.yaml` أو أي ملف متتبَّع بـ git
- ✅ **مسموح:** المفتاح في `~/.hermes/.env` فقط (مستثنى من git عبر `.gitignore`)
- ✅ الـ agent/LLM **ما يشوفش** المفتاح الخام — بياخده من environment variables

## 🔧 الإعداد (الحالي عندنا)

### 1. Hermes
- كل المفاتيح في `C:\Users\hshin\AppData\Local\hermes\.env`
- Hermes بيقرأها أوتوماتيك — ما نعدّلش `config.yaml` يدوياً
- ✅ `NVIDIA_API_KEY`, `OPENROUTER_API_KEY`, `NOTION_TOKEN`, `TMDB_API_KEY` كلها هناك

### 2. OpenCode
- `opencode.json` **مفيهوش أي مفتاح** — بس `baseURL` و `models`
- الـ launcher `opencode-nvidia.bat` بيحمّل كل `*_API_KEY` / `*_TOKEN` / `*_SECRET` من `.env` قبل ما يشغّل OpenCode
- ✅ لو فتحت OpenCode من غير الـ launcher، المفاتيح مش هتحمّل (أمان — مش هتشتغل من غير قصد)

## 📋 القواعد الصارمة (من factory_rules.md)
1. **ممنوع** مفتاح في الشات العام → يُعامل كـ **مسروق** ويُلغى فوراً
2. **ممنوع** `hardcode` في الكود → استخدم `os.environ` / `.env`
3. **ممنوع** commit لأي ملف فيه مفتاح → `.gitignore` بيشمل `*.env` + `*.hc` + `*api_key*`
4. المفاتيح القديمة (مثل NVIDIA الـ 3 القديمة) تُلغى من المصدر فوراً

## 🔄 مقارنة مع MindHub
| MindHub Credentials Vault | إعدادنا |
|---------------------------|---------|
| vault مش متاح للـ agent | `.env` مش متاح لـ OpenCode config ✅ |
| credentials مش في الـ config | opencode.json مفيهوش مفاتيح ✅ |
| open source (تقدر تفتّش الكود) | `.env` عندك محلياً ✅ |

## 🛡️ خطوات الطوارئ لو تسرب مفتاح
1. الغِ المفتاح من المصدر (build.nvidia.com / openrouter / notion.so/my-integrations)
2. أنشئ مفتاح جديد → حدّث `.env`
3. ابحث في git history عن التسريب → `git filter-branch` أو `BFG`
4. أعد الـ sync للـ vault (مفيش مفتاح في الـ commit أصلاً)
