---
type: report
title: 🔌 Zapier Actions + 🎤 SpeakoFlow — التنفيذ (2026-08-20)
tags: [zapier, speakoflow, voice, integration, windows, setup]
---
# 🔌 Zapier Actions + 🎤 SpeakoFlow (2026-08-20)

## 🔌 2. Zapier MCP (متصل — محتاج تفعيل actions)
- ✅ `zapier_mcp_bridge.py` متصل بـ Zapier MCP (التوكين في `.env`)
- ⚠️ **0 tools** حالياً — محتاج إنته تفعّل actions على الموقع

### خطوات التفعيل (30 ثانية):
1. افتح **https://zapier.com/mcp**
2. من **Connected Accounts** أضف: Gmail + Google Calendar + Notion (أو أي app)
3. فعّل الـ **actions** المحددة (مثلاً: "Send Email", "Create Calendar Event", "Update Notion Page")
4. أرجع هنا وأنا أشغّل `list-tools` تاني → هيظهروا

### لما تشتغل، هنقدر:
- نربط الـ Hermes/OpenClaw بـ 9000+ app
- cron job يبعت ملخص الصحة على Gmail أوتوماتيك
- الـ Dark Factory يحدّث Notion مباشرة

## 🎤 3. SpeakoFlow (صوت Windows — جاهز للتحميل)
- ✅ clone تم ✅ + لقيت رابط الـ release الأخير (v1.2.0)
- **رابط التحميل المباشر:**
  - 📥 exe: `https://github.com/AbhishekBarali/SpeakoFlow/releases/download/v1.2.0/SpeakoFlow_1.2.0_x64-setup.exe`
  - 📥 msi: `https://github.com/AbhishekBarali/SpeakoFlow/releases/download/v1.2.0/SpeakoFlow_1.2.0_x64_en-US.msi`
- **المميزات:** offline dictation + AI assistant + screen vision + Kokoro TTS (محلي!)
- **التثبيت:** double-click الـ exe → Next/Next → هيشتغل من الـ tray
- 📌 يكمّل `hermes_voice_local.py` (STT+TTS شغّال عبر uv)

### طريقة الاستخدام:
- اضغط hotkey (افتراضي hold لتسجيل) → تكلم → يتحوّل لنص/رد
- "Hey Flow" → يكتب الرد أو الإيميل ليك
- يربط بـ أي model (محلي أو مفتاحك)

---

## ✅ اللي اتعمل:
1. Zapier bridge محدّث (رسائل واضحة للتفعيل)
2. SpeakoFlow release link جاهز
3. التقرير محفوظ

## 📌 الخطوة الجاية منك:
- **Zapier**: فعّل actions على zapier.com/mcp → بلّغني أختبر الـ bridge
- **SpeakoFlow**: حمّل الـ exe وثبّته → بلّغني نجرّب الصوت
