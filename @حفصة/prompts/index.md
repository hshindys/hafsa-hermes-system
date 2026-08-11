# فهرس البرومبتات (Prompts Index)

## 📁 هيكل المجلد
```
prompts/
├── delaa_lines.md        # خطوط الدلع الكاملة (7× يومياً + تنويعات)
├── medical_reminders.md  # تذكيرات أدوية موحدة
├── tts_templates.md      # قوالب TTS للدلع والطقس
├── voice_tone.md         # دليل الصوت والنبرة (مرجع سريع)
└── persona_rules.md      # القواعد الصارمة (نسخة مختصرة)
```

## 🔗 روابط سريعة

| الملف | الوصف | يستخدم في |
|-------|--------|-----------|
| `delaa_lines.md` | 7 خطوط دلع أساسية + تنويعات صباحية/ظهرية/مسائية | `delaa_broadcast.py` |
| `medical_reminders.md` | نصوص تذكير أدوية صباحية/مسائية مدمجة في الروتين | `daily_routine.py`، كرون الروتين |
| `tts_templates.md` | قوالب النص المرسل لـ Kokoro (EN) | `delaa_broadcast.py::translate_to_english()` |
| `voice_tone.md` | ملخص 4 أوضاع: خاص/عائلي/تقني/إبداعي | كل الوكلاء |
| `persona_rules.md` | القواعد الـ 4 المحظورة + مرجع سريع | system prompt، كل المحادثات |

## 📋 كيفية الاستخدام في الكود

### في `delaa_broadcast.py`:
```python
# استيراد الخطوط من ملف خارجي (اختياري - حالياً hardcoded)
from pathlib import Path
DELAA_FILE = Path(__file__).parent.parent / "Hafsa" / "@حفصة" / "prompts" / "delaa_lines.md"
```

### في `daily_routine.py`:
```python
# تذكيرات الأدوية مدمجة في القسم المولّد
# راجع: prompts/medical_reminders.md للنصوص المعيارية
```

### في System Prompt للـ Agent:
```
@حفصة/persona_rules.md  ← القواعد الصارمة
@حفصة/prompts/voice_tone.md  ← الصوت والنبرة لكل سياق
```

## 🔄 تحديث البرومبتات
- عند إضافة سطر دلع جديد: ضيفه في `delaa_lines.md` وحدث `DELAA_LINES` في `delaa_broadcast.py`
- عند تغيير نبرة: حدث `voice_tone.md` و `@حفصة_.md` قسم "الصوت والنبرة"
- عند إضافة قاعدة: حدث `persona_rules.md` و `@حفصة_.md` قسم "القواعد الصارمة"

---

*آخر تحديث: 2026-08-11 — د. حفصة*