---
type: rules
title: 🎯 Vibe Coding Playbook — قواعد الـ Dark Factory
tags: [vibe-coding, dark-factory, rules, review, planning, slop-prevention]
---
# 🎯 Vibe Coding Playbook — قواعد للـ Dark Factory

> مستوحى من "Vibe Coding Playbook" (الفيديو: Tim & Andrew Top 10 GitHub Repos).
> الفكرة: الـ agent = junior engineer. السرعة تمام، بس من غير "slop" (كود متراكم من غير قرار).

## القواعد (تُطبّق على أي مهمة كود في الـ Dark Factory):

### 1. خطّط قبل أي سطر كود
- قبل الكتابة: اكتب **PLAN** (الهدف + الخطوات + الملفات اللي هتتعدّل)
- لو المهمة معقّدة → اسأل المستخدم أسئلة توضيحية أولاً (زي Grill Me)
- ممنوع `write_file` مباشرة على ملف كبير من غير خطة

### 2. اتبع الـ patterns الموجودة
- اقرأ الكود الحالي قبل تعديله (لا تبتكر style جديد)
- استخدم نفس التسميات/conventions الموجودة في المشروع
- لو فيه abstraction موجود، استخدمه (متكرّرش)

### 3. review إلزامي قبل الـ push/التسليم
- بعد الكتابة: افحص الكود (error handling موجود؟ null checks؟)
- شغّل الـ tests لو موجودة
- لو فيه `no-op` أو كود ميت ← احذفه (زي pruning_checker)
- **ممنوع تسليم كود من غير مراجعة ذاتية**

### 4. تقليل الـ slop
- كل سطر كود = قرار واعٍ (مش مجرد "الـ agent كتبه")
- لو مش متأكد من pattern ← اسأل، متخمّنش
- سجّل القرارات في الـ PR/commit message

### 5. التدرّج
- ابدأ بـ MVP صغير يشتغل ← وسّع بالتدريج
- متحاولش تحل كل المشكلة في ضربة واحدة

### 6. Prompt-to-Plugin (من DeepSeek Harness)
- الـ agent ممكن **ينشئ skill/plugin جديد من وصف باللغة الطبيعية** (Creator Mode)
- لو المستخدم طلب feature جديد: اكتب SKILL.md + السكريبت، وثبّته في `~/.hermes/skills/`
- اسم الـ skill بـ kebab-case، يكون فيه `frontmatter` (name/description) + خطوات واضحة
- سجّل الـ creation في الـ agent_trace (kind=plugin_create)

## 🔗 العلاقة بباقي الأنظمة:
- **Grill Me**: يغطّي "اسأل قبل تبدأ" (القاعدة 1)
- **pruning_checker**: يغطّي "احذف الـ no-ops" (القاعدة 3/4)
- **Dark Factory**: بيشغّل الـ coding agents ← القواعد دي بتحكمهم
- **memory_graph**: بيساعد الـ agent يفهم المشروع قبل يكتب (زي GraphiPy)
- **agent_trace**: بيسجّل كل interaction (prompts/reasoning/tool calls) للشفافية
- **Prompt-to-Plugin**: يكمّل إنشاء الـ skills أوتوماتيك (زي DeepSeek Creator Mode)

## 📌 تفعيل:
- هذه القواعد تُقرأ تلقائياً في أي session بيعمل coding (عبر الـ skill أو الـ AGENTS.md)
- أي agent في الـ Dark Factory لازم يتبعها
