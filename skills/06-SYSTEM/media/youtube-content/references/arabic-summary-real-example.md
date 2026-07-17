# Real Example: Arabic Structured Summary with Priorities

This is the actual output format used when summarizing a video about AI agent use cases (YouTube: https://www.youtube.com/watch?v=6BHh8BoKim4).

## Full Output

```markdown
## 📋 ملخص الفيديو
حلقة تفاعلية (reaction video) بين أندرو وإريك سو عن استخدامات عملية لـ Hermes agent. 
قدم 5 من رواد الأعمال استخداماتهم العملية.

## 🔍 الاستخدامات العملية (مرتبة حسب الأولوية)
| # | الشخص | الاستخدام | ملاحظات |
|---|---|---|---|
| 1 | أندرو | سوم كمبيوتر - Copy Google Loop | إعطاء prompt لـ Hermes على الديسكتوب يتحكم في Claude Code ويكرر اللوب لحد ما يخلص المهمة. يشتغل بالليل بدون تدخل. |
| 2 | أليكس | بحث عن المنافسين (Creator Buddy) | prompt بسيط → فتح براوزر → بحث تقني كامل عن موقع منافر + markdown → إيداعه لـ Claude Code لبناء features مماثلة. |
| 3 | إريك | Resolver (تصميم أولويات) | يراقب كل الشغل عبر Cloud Code + Codeex + Hermes → يطلع قائمة أولويات يومية ويحدد إيه اللي يتعمل فيه loop. |
| 4 | إريك | Wiki ذاكرة يومية | يحط كل قراراته اليومية في system زي Obsidian مع QMD memory عشان Hermes يقدر يرجع لها. |
| 5 | نيت هيرك | HyperFrames - فيديو بـ AI | يطلب من Hermes يعمل فيديو باستخدام أدوات الـ video editing البحث بنفسه عن الأداة وتثبيتها. |
| 6 | إريك | Zapier MCP - Email Automation | يتصل بالإيميل ويرسل follow-ups تلقائي بعد كل video ينتشر. |
| 7 | إريك | Cron Jobs يومية | Daily AI news، YouTube comment monitoring/reply، morning business summary، server checks، follow-up reminders. |
| 8 | شاري bell | Hermes يعمل Interview معاك | الـ agent بيسألك أسئلة عشان يفهمك ويقدر يشتغل معاك بشكل أفضل. |
| 9 | إريك | Skill-ification (حقول المهارة) | بعد كل مشروع كبير، يحفظ الـ workflow كـ skill عشان يكرره بدون re-prompt. |

## 🎯 مفاهيم رئيسية
| المفهوم | الوصف |
|---|---|
| Loop | تكرار مهمة لحد ما تخلص، يشتغل بالليل |
| Cron Job | مهمة مجدولة (يومية/أسبوعية) تنفذ تلقائياً |
| Resolver | نظام يراقب شغلك ويطلع أولويات |
| QMD Memory | أداة ذاكرة خارجية (Obsidian + QMD) لتحسين أداء الـ agent |
| Zapier MCP | ربط الـ agent بالإيميل وتطبيقات تانية |
| Skill | تحويل workflow لـ skill قابل لإعادة الاستخدام |
| Grill Me | skill أسئلة بتحاور المستخدم عشان تساعده يعبر عن اهدافه |
| Desktop App | نسخة الديسكتوب فيها pin + categorize sessions |
| Gateway | تحكم عن بعد في agent على device تاني |
| Tail Scale | شبكة خاصة بين عدة أجهزة عبر SSH |

## 💡 اقتراحات للتطبيق (مرتبة بالأولوية)
| الأولوية | التطبيق | كيف |
|---|---|---|
| ⭐⭐⭐ | Loop | استخدمها لمهام طويلة (بحث، بناء، تحديث) — خليه يشتغل بالليل |
| ⭐⭐⭐ | Resolver | اعمل cron يراقب شغلك ويفكرك بالأولويات آخر اليوم |
| ⭐⭐⭐ | Cron + Zapier | اربط الإيميل عشان يبعت follow-ups تلقائي |
| ⭐⭐ | QMD Memory | حسن ذاكرة الـ agent بأدوات خارجية (أو استخدم Vault بتاعك) |
| ⭐⭐ | Skill-ification | كل ما تخلص مشروع مفيد، احفظه skill |
| ⭐⭐ | Grill Me | اسأله أسئلة عنك عشان يفهم أسلوبك وأولوياتك |
| ⭐ | Gateway + Tail Scale | لو عندك عدة أجهزة، شبكهم |
| ⭐ | HyperFrames Video | جربه لفيديوهات قصيرة مع النصوص |

## ⚠️ تحذيرات مهمة
- Kanban Board في الـ desktop app لسه مش mature — استخدم Notion بدل منه
- الـ daily briefing ممكن يبقى overkill ـ الإجماع: استخدم بس اللي فعلاً تحتاجه
- متحملش SSDs كتير — الاستخدام المفرط ممكن يحرق الهارد
- Slack مش ideal للـ single player — استخدم Discord لو لوحدك
- حق الملفات المحفوظة على الكمبيوتر — ارفعها على Notion/Vault عشان تقدر توصلها
```

## When to use this enhanced format

Use when the video content is about:
- AI tools / workflows / use cases
- Productivity / personal development
- Software development practices
- Any content with actionable takeaways

The key addition beyond the basic format is: **priority-ranked suggestions table** and **warnings section**.
