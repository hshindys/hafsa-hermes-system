---
type: project
name: Shared Memory Hub (دماغ الفريق المشترك)
status: active
started: 2026-08-07
tags: [ai, agents, memory, hermes]
---
# 🧠 مشروع: Shared Memory Hub — دماغ الفريق المشترك لـ Agents

> فكرة من فيديو "Top 10 GitHub repos" (TencentDB Agent Memory — الـ repo #1، 17.4K ⭐)
> وامتدادها في فيديو "Second Brain vs Shared Brain" (Day AI). بنته هفصة فعلياً وشغّال.

## الهدف
دماغ واحد مشترك كل agent و cron job و chat session يغذّيه — أي agent جديد يبدأ "من 60 مش 0"
عشان ما يضطرش حاتم يعيد شرح السياق كل مرة (SOPs، خلفية المشاريع، تفضيلات).

## المعمار (4-layer pyramid — L0 → L3)
- **L0 Conversation** — المحادثات الخام (SQLite + FTS5).
- **L1 Atomic** — حقائق/تفضيلات مستخرجة ومفلترة (dedup sha256).
- **L2 Scene** — بلوكات markdown لكل جلسة.
- **L3 Persona** — تجميع التفضيلات في `persona/<team>/<user>.md`.

## الاستخراج (L0 → L1)
- لو `MEMORY_HUB_LLM_API_KEY` + `MEMORY_HUB_LLM_BASE_URL` → موديل OpenAI-compatible رخيص.
- غير كده → مستخرج heuristic مدمج (لا شبكة، لا مفتاح).

## المسار والملفات
- المحرك: `C:\Users\hshin\AppData\Local\hermes\shared_memory\memory_hub.py`
- الـ gateway (v3-compatible): `C:\Users\hshin\AppData\Local\hermes\shared_memory\server.py`
- التوثيق: `...\shared_memory\README.md`
- التخزين: `%USERPROFILE%\.memory-tencentdb\memory-tdai` (أو `TDAI_DATA_DIR`).

## التشغيل
```bash
"C:\Users\hshin\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" server.py --host 127.0.0.1 --port 8420
```

## الـ API (متوافق مع /v3/* للبلاجن الرسمي)
`/health` · `/v3/conversation/add` · `/v3/conversation/search` · `/v3/atomic/search`
`/v3/scenario/ls` · `/v3/recall` · `/v3/session/end`
كل endpoint بياخد `team_id` / `agent_id` / `user_id` لعزل الذاكرة.

## نشاط اليوم (2026-08-07 / 08)
- [x] لخّص فيديو "Top 10 GitHub repos" وطلّع الأولويات → الأهم: TencentDB Agent Memory.
- [x] بنى `memory_hub.py` (L0→L3، SQLite+FTS5، stdlib بس).
- [x] بنى `server.py` gateway متوافق مع `/v3/*` على 127.0.0.1:8420.
- [x] شغّل واختبر فعلياً: pipeline ملأ L0/L1/L2، recall رجّع persona+facts،
      وHTTP endpoints كلها رجعت نتائج صحيحة (add/recall/atomic-search/conversation-search/scenario-ls).
- [x] لخّص فيديو "Second Brain vs Shared Brain" (Day AI) وربط الفكرة بالـ hub.
- [x] حدّث [[../@حفصة/@حفصة_]] بملف نشاط اليوم.

## الخطوات الجاية (مقترحة)
- [x] ربط الـ vault ده (`D:\\vaults\\Hafsa`) كـ L0/L2 source للـ hub — تم ✅.
- [x] إضافة change-set log (rollbacks) زي ما الفيديو التاني اقترح (فكرة Karpathy) — تم ✅.
- [ ] ربط cron الأدوية بالـ hub عشان الـ bot يفتكر "لا seafood + Concor 05:00" من غير تكرار.
- [ ] اختياري: تفعيل استخراج LLM لو توفّر مفتاح OpenAI-compatible.

## ربط الـ Vault (تم 2026-08-08)
- دالة `vault_ingest()` بتمشي على `D:\\vaults\\Hafsa` وتدخل كل ملف markdown كـ L0 (محدد
  بالفولدرات: 🎯 المشاريع / 👤 حفصة / 📅 اليوميات / 🧠 المعرفة / 💡 الأفكار / 📚 المصادر).
- بتستخرج حقائق L1 (heuristic، عربي+إنجليزي) وتبني L3 persona تلقائياً.
- بتسجّل change-set entry عند كل ingest (للـ rollback/audit).
- تشغيل: `python memory_hub.py ingest-vault "D:/vaults/Hafsa" hafsa-vault`
  أو عبر API: `POST /v3/vault/ingest {"vault_path":"D:/vaults/Hafsa","team_id":"hafsa-vault","user_id":"hatem"}`
- **تحقق فعلي:** ingest=72 ملف، recall بيرجّع persona (11 تفضيل)، atomic بيرجّع
  "ممنوع نهائي: أكل بحري على حاتم" صح. (ملاحظة: المسار في JSON يُكتب بـ forward slash
  `D:/vaults/Hafsa` لتفادي escape مشاكل في JSON.)

## العلاقة بالبلاجن الرسمي
البلاجن الرسمي (`TencentCloud/TencentDB-Agent-Memory`) محتاج hermes source tree + بناء Node gateway
ثقيل (`node-llama-cpp`, `sqlite-vec`, `jieba`) + مفتاح LLM. هذا hub مستقل بيعمل نفس الوظيفة
ويمكن استبداله بالـ Node sidecar لاحقاً من غير تغيير النداءات.

## روابط
- الوكيل: [[../@حفصة/@حفصة_]]
- تقارير مشابهة: [[AI-Agent-Improvement-Report]]
