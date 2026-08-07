# CLAUDE.md — Hafsa Agent Vault Router

> هذا الملف هو الـ Router الرئيسي لخزنة حفصة.
> اقرأه أولاً قبل أي تفاعل مع الخزنة.

---

## ⚠️ تعليمات للـ AI Agent

1. **اقرأ هذا الملف أولاً** — هو بوابة الدخول لكل شيء
2. **حدد الموضوع** — شخصية؟ مشروع؟ فكرة؟ معرفة؟
3. **اذهب للملف المناسب** من الفهرس أدناه
4. **أجب بناءً على الملفات** — لا تخترع معلومات
5. **لا تحذف أي حاجة** — انقل للأرشيف بدل الحذف
6. **كل ملف جديد** — أضفه للفهرس المناسب

---

## 📂 الـ Vaults المتاحة

| الـ Vault | الـ Path | الوصف |
|----------|---------|-------|
| **Hafsa** | `C:/Users/hshin/OneDrive/Documents/Hafsa/` | خزنة حفصة — الهوية والشخصية |
| **Hatem Nad** | `C:/Users/hshin/OneDrive/Documents/Hatem Nad/` | خزنة حاتم — Second Brain |

---

## 📖 فهرس خزنة حفصة (Hafsa)

| المجلد | الوصف |
|--------|-------|
| `@حفصة/` — الهوية، الشخصية، القيم، الأهداف، الروتين |
| `🎯 المشاريع/` — المشاريع الحالية والتقارير |
| `💡 الأفكار/` — بنك الأفكار، كتابة، تصميم |
| `👥 الأشخاص/` — العائلة والعمل |
| `🧠 المعرفة/` — تقنية، طب، لغات، أديان، رحلات، تاريخ، تراجم |
| `📅 اليوميات/` — يوميات + قوالب |
| `📰 تقارير/` — بحوث وتقارير |
| `💊 طبي/` — ملاحظات صحية (مرجع) |
| `🍽️ World Cuisine/` — أكاديمية المطابخ العالمية (15 مطبخ) |
| `🍳 Food/` — وصفات سريعة صحية |
| `🎵 Music/` — الموسيقى والصوتيات |
| `⏰ Cron/` — المهام المجدولة |

---

## 📖 فهرس خزنة حاتم (Hatem Nad)

| المجلد | الوصف |
|--------|-------|
| `01-أجندات دين/` — أذكار وعبادات ونوايا |
| `02-مفكرة/` — يوميات وخواطر |
| `03-ملاحظات/` — ملاحظات سريعة |
| `04-تقويم/` — جدول أسبوعي |
| `05-كالندر/` — تقويم شهري بصري |
| `06-جداول حسابية خاصة/` — مصاريف وديون واستثمارات |
| `04-Projects/` — مشاريع إبداعية (كرون، Second Brain) |
| `05-Ideas/` — بنك الأفكار |
| `03-Resources/` — مراجع وموارد |
| `07-Tools/` — أدوات AI |
| `Templates/` — قوالب جاهزة |
| `رواية-كرون/` — مشروع رواية كرون |

---

## 🧠 المكتبة الشاملة

> ١,٠٣٣ كتاب مستخرج من المكتبة الشاملة المحلية

| القسم | العدد | المكان |
|-------|-------|--------|
| الفرق والردود | ١٥١ | `🧠 المعرفة/دراسات مقارنة الأديان/` |
| التاريخ | ٢٠٦ | `🧠 المعرفة/` |
| التراجم والطبقات | ٥٧٩ | `🧠 المعرفة/` |
| البلدان والرحلات | ٩٧ | `🧠 المعرفة/كتب الرحلات والعجائب/` |

---

## 📝 قواعد الاستخدام

1. **لا تحذف أي حاجة** — انقل للأرشيف بدل الحذف
2. **كل ملف جديد** — أضفه للفهرس المناسب
3. **اليوميات** — تُكتب يومياً في `📅 اليوميات/`
4. **الأفكار** — تُضاف لـ `💡 الأفكار/Bank of Ideas.md`
5. **الـ frontmatter** — كل ملف لازم فيه frontmatter

---

## 🔗 الـ Symlinks

- `vault-hafsa` → `C:/Users/hshin/OneDrive/Documents/Hafsa/`
- `vault-hatem-nad` → `C:/Users/hshin/OneDrive/Documents/Hatem Nad/`

## 🧠 الـ LLM Wiki System

> Self-improving knowledge base — Hermes forgets, the Vault remembers.

| Component | What | Schedule |
|-----------|------|----------|
| `vault-wiki` skill | Read/write/query all vaults | Always loaded |
| Vault Health Check | Daily index audit | 7:00 AM daily |
| Knowledge Digest | Weekly summary | Sunday 10:00 AM |
| Memory Sync | Daily vault stats + journal | 11:00 PM daily |

### Vault Wiki Skill
- **Location:** `~/.hermes/profiles/hafsa/skills/vault-wiki/SKILL.md`
- **Purpose:** Unified knowledge base across Hafsa + Hatem Nad vaults
- **Search:** Always check BOTH vaults before answering
- **Write:** Every new note gets frontmatter + index entry

---

*آخر تحديث: ٢٥ يونيو ٢٠٢٦*
