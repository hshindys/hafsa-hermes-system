# 🔍 Skills Audit — 2026-06-24

> بناءً على فيديو GitHub Trending + احتياجاتنا من OODA/Infinite Brain

## 📊 الإحصائيات
- **إجمالي Skills:** 106 SKILL.md في 33 category
- **مستخدم فعلياً:** ~35 skill
- **مرشح للحذف/أرشفة:** ~40 skill
- **يحتاج تحديث:** ~15 skill
- **أمني (يحتاج scan):** كل الـ skills الجديدة

---

## ✅ CORE — لازم تبقى (35 skills)

### Medical (7)
| السبب | الاسم | الحالة |
|---|---|---|
| بحث طبي أساسي | medical-research | ✅ نشط |
| توليد skills طبية | medical-research-skill-pipeline | ✅ نشط |
| تلخيص أبحاث | medical-research-synthesis | ✅ نشط |
| تشخيص باطنة | internal-medicine-ai-diagnosis | ✅ نشط |
| أورام دماغية | neurology-ai-brain-tumor-diagnosis | ✅ نشط |
| تحليل شبكية | ophthalmology-ai-retinal-analysis | ✅ نشط |
| مراجعة ملفات | medical-chart-review | ✅ نشط |

### Writing & Novel (4)
| السبب | الاسم | الحالة |
|---|---|---|
| رواية كرون | novel-writing | ✅ نشط |
| كتابة إبداعية | creative-writing | ✅ نشط |
| سرد متقدم | master-storyteller | ✅ نشط |
| بناء عوالم | world-building | ✅ نشط |

### Voice & Audio (4)
| السبب | الاسم | الحالة |
|---|---|---|
| صوت حفصة | voicebox | ✅ نشط |
| نسخ صوت | voice-cloning | ✅ نشط |
| pipeline صوت | voice-cloning-pipeline | ✅ نشط |
| MOSS TTS | moss-tts-voice-cloning | ✅ نشط |

### Knowledge & Search (4)
| السبب | الاسم | الحالة |
|---|---|---|
| إنترنت | agent-reach | ✅ نشط |
| خزنة | vault-wiki | ✅ نشط |
| ربط خزنة | vault-integration | ✅ نشط |
| إعادة هيكلة | vault-restructuring | ✅ نشط |

### Productivity (6)
| السبب | الاسم | الحالة |
|---|---|---|
| نتائج مباريات | sports-scores | ✅ نشط |
| أخبار | hafsa-news-oracle | ✅ نشط |
| أخبار تلقائية | hermes-news-sweep | ✅ نشط |
| GitHub | github-* (6 skills) | ✅ نشط |
| إعدادات | hermes-agent | ✅ نشط |
| أمن | skill-specter | ✅ نشط |

### Agents & Orchestration (4)
| السبب | الاسم | الحالة |
|---|---|---|
| Multi-agent | deer-flow-superagent | ✅ نشط |
| Dashboard | agentic-os-dashboard | ✅ نشط |
| Personas | persona-system | ✅ نشط |
| Documents | document-hub | ✅ نشط |

### Research (3)
| السبب | الاسم | الحالة |
|---|---|---|
| arXiv | arxiv | ✅ نشط |
| LLM Wiki | llm-wiki | ✅ نشط |
| Polymarket | polymarket | ✅ نشط |

### Media (3)
| السبب | الاسم | الحالة |
|---|---|---|
| YouTube | youtube-content | ✅ نشط |
| Images | image-gen | ✅ نشط |
| Blogs | blogwatcher | ✅ نشط |

---

## 🔄 NEEDS UPDATE — محتاج تحديث (15 skills)

| الاسم | المشكلة | الإجراء |
|---|---|---|
| agent-reach | ممكن يحتاج update للـ backends | شغّل `agent-reach check-update` |
| voice-cloning | تكرار مع voice-cloning-pipeline | ادمج مع pipeline |
| moss-tts-voice-cloning | تكرار مع voice-cloning | احذف أو أرشف |
| github-code-review | ممكن يحتاج تحديث للـ API | راجع rate limits |
| github-issues | ممكن يحتاج تحديث | راجع |
| github-pr-workflow | ممكن يحتاج تحديث | راجع |
| nano-pdf | ممكن يكون محدود | جرب بدائل |
| teams-meeting-pipeline | مش مستخدم بكثرة | جرب أو أرشف |
| google-workspace | مش مستخدم بكثرة | جرب أو أرشف |
| apple/* | مش على macOS | أرشف أو احذف |
| computer-use | مش مستخدم | أرشف |
| hyperframes | مش مستخدم | أرشف |
| comfyui | موجود image-gen أقوى | أرشف |
| manim-video | مش مستخدم | أرشف |
| p5js | مش مستخدم | أرشف |

---

## 🗑️ REDUNDANT — مكرر/مش مستخدم (25 skills)

### Voice (3 → خلي واحد)
- voice-cloning + moss-tts-voice-cloning + voice-cloning-pipeline → **خلي voice-cloning-pipeline بس**

### Design (8 → خلي 2-3)
- popular-web-designs + glm-open-design-system + taste-skill-anti-slop + humanizer → **خلي glm-open-design-system + humanizer**
- sketch + claude-design + pretext + excalidraw + architecture-diagram + ascii-art + ascii-video + baoyu-infographic + design-md → **خلي claude-design + excalidraw**

### Creative (6 → خلي 2)
- creative-intelligence-empire + songwriting-and-ai-music + heartmula + gif-search + songsee → **خلي heartmula بس**

### Research (3 → خلي 2)
- polymarket + arxiv + llm-wiki + blogwatcher → **خلي arxiv + blogwatcher**

### Productivity (5 → خلي 2)
- notion + airtable + powerpoint + maps + ocr-and-documents → **خلي notion + ocr-and-documents**

---

## ⚠️ SECURITY RISK — محتاج Scan (كل الـ skills الجديدة)

| الاسم | المخاطر | الإجراء |
|---|---|---|
| أي skill جديد من GitHub | prompt injection, data exfiltration | شغّل skill-specter قبل التثبيت |
| agent-reach | بيانات cookies | راجع الـ permissions |
| voicebox | ملفات صوت محلية | تأكد من الـ access |
| blogwatcher | RSS parsing | تأكد من input validation |

---

## 🎯 التطبيق الفوري

### 1. Skills Folder Structure (OODA)
```
~/.hermes/skills/
├── 00-CORE/          # الأساسية (medical, writing, voice, search)
├── 01-PROJECTS/      # مشاريع نشطة (sports, news, agents)
├── 02-RESEARCH/      # أبحاث (arxiv, polymarket, blogs)
├── 03-CREATIVE/      # إبداع (design, music, art)
├── 04-PRODUCTIVITY/  # إنتاجية (notion, PDF, workspace)
├── 05-ARCHIVE/       # قديم/مش مستخدم
└── 06-SYSTEM/        # تشغيل (hermes-agent, skill-specter)
```

### 2. Agent Reach Update
- شغّل `agent-reach check-update`
- لو في update، طبقه

### 3. Voice Skills Consolidation
- احذف `moss-tts-voice-cloning` و `voice-clocking`
- خلي `voice-cloning-pipeline` هو الأساسي

### 4. Security Scanning
- شغّل skill-specter على كل الـ skills اللي مش متأكد منها

### 5. New Skills from Video
- مفيش skills جديدة محتاجة تنزيل — اللي عندنا كافي
- بس نقدر نعمل skill جديدة: **codebase-memory-mcp** (من الفيديو)
