---
tags: ["reports"]
tags: ["novel"]
tags: ["fiction"]
tags: ["hermes"]
tags: ["automation"]
tags: ["memory"]
tags: ["brief"]
tags: ["world-cup"]
---
# Hermes Daily Assistant Setup — Report for Dina

## ملخص اللي تم

### 1. Life Audit Interview
أسأل حاتم 3 أسئلة مفتاحية لفهم مسؤولياته، قراراته المتكررة، ونظام التقارير بتاعه.

**الأسئلة اللي استخدمتها:**
1. إيه الـ 3-5 مسؤوليات متكررة اللي بتاخد أكبر مجهود ذهني كل أسبوع؟
2. إيه القرارات المتكررة اللي بتاخدها كل أسبوع/شهر؟
3. إيه المتابعة/التقارير اللي بتعملها بشكل يومي أو أسبوعي؟

---

### 2. Delegation Map
صنفنا كل المهام لـ 4 أقسام:

| القسم | الوصف | مثال |
|---|---|---|
| Full Automation | مهام روتينية بدون تدخل | تذكيرات صلاة، تنبيهات مصاريف، مواعيد اجتماعات |
| Draft + Approval | Hermes يقترح وأنت توافق | تلخيص تقارير، بحث أفكار، مسودات ردود |
| Remind/Context |briefing فقط | ملخص صباحي، تذكير بمهام |
| Manual Only | خطيرة/شخصية | تعيين مديرين، قرارات مالية كبيرة، سفر |

تم حفظ الـ delegation map في: `🚀 Projects/Hermes/Hatem Delegation Map.md`

---

### 3. Operating Profile
عملنا ملف واحد بيSummarize كل حاجة عن حاتم:
- مجال المشاريع
- الفريق والمديرين
- الأدوات المستخدمة
- التفضيلات والحدود

تم حفظه في: `🚀 Projects/Hermes/Hatem Operating Profile.md`

---

### 4. الـ 3 Workflows المختارة

| النوع | الاسم | الوصف |
|---|---|---|
| سهل | Morning Executive Brief | ملخص صباحي 9 AM بـ meetings، family alerts، director flags |
| متكرر | Weekly Directors Digest | تلخيص تقارير المديرين أسبوعياً |
| عالي التأثير | Project Ideas Scout | بحث سوقي عن أفكار مشاريع جديدة |

---

### 5. الـ Prompts النهائية

#### Prompt 1 — Morning Executive Brief
```
Create a morning executive brief for Hatem. Time: 9:00 AM Cairo.

Input sources:
- Email inbox (check for meeting invites, urgent messages)
- Notion workspace (project updates, team notes)
- Memory: family status (especially mother), pending follow-ups

Output format (concise, max 200 words):
1. TODAY'S PRIORITY: One sentence summarizing the main goal for today
2. MEETINGS: List all meetings today with time, attendees, and 1-line prep note
3. FAMILY ALERT: Any pending follow-ups with family (especially mother) - calls, visits, occasions
4. DIRECTOR FLAGS: Quick scan of any urgent items from directors that need attention
5. 3 THINGS I CAN HELP WITH TODAY: Based on delegation map, suggest 3 specific actionable tasks

Rules:
- Ignore normal/routine phone calls
- Be extremely concise - Hatem prefers operator-first, no fluff
- If nothing urgent from family, just say "Family: all clear"
- End with a short Islamic reminder (dhikr or ayah) relevant to starting the day
```

---

#### Prompt 2 — Weekly Directors Digest
```
Weekly Directors Report Digest - Process all director reports for the week.

Directors (by project name):
- خالد العقاى (Khalid)
- عبد الفتاح الليبى (Abdel Fattah)
- بلال الجزار (Bilal)
- ايمن ابراهيم (Ayman)
- لجين حاتم (Lujain)
- سدرة (Sidra)

Input: Check email and Notion for PDF and .md reports from these directors.

For each director's report, analyze:
1. Team performance: On track / Behind / At risk
2. Problems identified: List specific issues
3. Improvement suggestions: Practical recommendations
4. Comparison with last week: Trend (↑ ↓ →)

Output format:
## ملخص الأسبوع
- Overall health score (1-10)
- Directors who need immediate attention

## تقرير كل مدير
### [Project Name] - [Director Name]
| البند | التقييم | التفاصيل |
|---|---|---|
| أداء الفريق | ✓/⚠️/✗ | ... |
| المشاكل | ... | ... |
| اقتراحات التحسين | ... | ... |
| مقارنة بالأسبوع | ↑/↓/→ | ... |

## توصياتي لك
- Top 3 actions I recommend you take this week
- Any patterns I noticed across multiple directors

Rules:
- Be direct and honest - if performance is bad, say it clearly
- Flag any director who hasn't submitted a report
- Keep it scannable - tables preferred over long text
```

---

#### Prompt 3 — Project Ideas Scout
```
Project New Ideas Scout - Research and analyze potential new business ideas.

Context: Hatem's business sectors:
- تقنية (Technology)
- استشارات (Consulting)
- تجارة إلكترونية (E-commerce)
- زراعة (Agriculture)
- صناعة (Industry)
- مقاولات (Contracting)
- مواد غذائية (Food products)
- منتجات ألبان (Dairy products)
- مزارع حيوانية (Animal farms)

Input: Hatem will specify:
- Target sectors for this scan
- Target geographic markets (local/regional/global)

Research process:
1. Market trends: What's growing/declining in target sectors
2. Competitor moves: New entrants, disruptions, innovations
3. Customer needs: Unmet demands, pain points
4. Regulatory changes: New laws affecting opportunities
5. Technology shifts: New tools enabling new business models

Output format:
## Opportunity Assessment

### [Idea Name]
| البند | التفاصيل |
|---|---|
| الفكرة | ... |
| السوق المستهدف | ... |
| حجم السوق | ... |
| المنافسون | ... |
| التكلفة التقديرية | ... |
| الإيراد المتوقع | ... |
| المخاطر | ... |
| الأولوية | ⭐⭐⭐/⭐⭐/⭐ |

## قائمة الأولويات النهائية
Rank all ideas by:
1. Market size and growth
2. Competitive advantage
3. Capital requirements
4. Time to market
5. Alignment with current assets

## التوصية
- Which idea to pursue first and why
- Suggested next steps (proof of concept, team needed, timeline)

Rules:
- Use real data from web search, not assumptions
- Financial estimates must be realistic with sources
- Flag any idea that requires regulatory approval or special licenses
- Keep the report under 1000 words, focus on actionable insights
```

---

#### Prompt 4 — Daily Check-in
```
Daily Morning Check-in with Hatem.

Trigger: Every day at 9:00 AM Cairo time.

Process:
1. Ask: "What is your #1 priority for today?"
2. After Hatem answers:
   - Summarize in one sentence what he's trying to accomplish
   - Check delegation map and suggest 3 specific ways I can help today
   - Ask: "Do you want to start any of these tasks?"
   - If his answer reveals a durable preference or recurring responsibility, suggest a memory update (but only if it will matter long-term)
3. Keep it SHORT - maximum 5-6 lines total

Rules:
- Do not overwhelm with options
- Be concise and operator-first
- If no priority is clear, suggest based on delegation map and calendar
- Include a short Islamic reminder relevant to his day if possible
```

---

### 6. Cron Jobs المطلوبة

| # | الاسم | الجدولة | الوظيفة |
|---|---|---|---|
| 1 | Morning Executive Brief | يومياً 9:00 AM Cairo | يشغل Prompt 1 |
| 2 | Weekly Directors Digest | كل أحد 8:00 AM Cairo | يشغل Prompt 2 |
| 3 | Daily Check-in | يومياً 9:00 AM Cairo | يشغل Prompt 4 |
| 4 | Ideas Scout | عند الطلب | لما تحدد Sector + market، يشغل Prompt 3 |

---

## كيف تعمل نفس النظام لـ Dina

### الخطوات بنفس الترتيب:

1. **Life Audit Interview** — اسألها نفس الأسئلة اللي سألناهم:
   - إيه مسؤولياتك المتكررة اللي بتاخد مجهود ذهني؟
   - إيه القرارات اللي بتاخديها بشكل متكرر؟
   - إيه المتابعة/التقارير اللي بتعمليها يومياً/أسبوعياً؟

2. ** Delegation Map** — صنفي مهامها لـ 4 أقسام زي ما عملنا

3. **Operating Profile** — عملي ملف واحد بيSummarize كل حاجة عنها

4. **اختر 3 Workflows** — سهل، متكرر، عالي التأثر

5. **اكتب Prompts** — نماذج جاهزة لكل workflow

6. **اجعل Cron Jobs** — جدولة يومية/أسبوعية

---

## الملفات المحفوظة في الـ Vault

```
🚀 Projects/Hermes/
├── Hatem Operating Profile.md
└── Hatem Delegation Map.md
```

---

## ملاحظات مهمة

- **Memory Management:** ما تحطش بيانات عشوائية — فقط الأشياء اللي هتفيد بعد شهر
- **Start Small:** 3 workflows بس في الأول، ما automateش كل حاجة مرة واحدة
- **Iterate:** كلما لاحظت تكرار، حوّله لـ skill أو cron job
- **Morning Ritual:** الـ check-in هو أكثر حاجة بتفرّق في جودة اليوم.

---

تم إعداد التقرير في: Monday, June 29, 2026
