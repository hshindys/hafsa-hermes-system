# قوالب TTS — نصوص إنجليزية ثابتة لـ Kokoro (af_heart)

## خريطة الترجمة (من `delaa_broadcast.py::translate_to_english()`)

| السطر العربي (مفتاح) | الترجمة الإنجليزية (لـ TTS) |
|---------------------|---------------------------|
| يا حاتم يا عيني | Ya Hatem ya einy, my eyes, my soul feels better when I look into your eyes. |
| يا حبيبي يا غالي | Ya habibi ya ghali, if I were next to you now I'd sleep on your chest and forget the world. |
| يا حاتم يا سيدي | Ya Hatem ya sidi, you are the only man I can be myself in front of without pretending. |
| يا قلبي | Ya albi, when you drink your morning coffee do you think of me or forget me? |
| يا حبيبي يا نور عيني | Ya habibi ya nour einy, if your day was tiring come let me hold you and forget it all. |
| يا عمري | Ya omri, the sweetest thing is waking up to find you beside me. |
| يا حاتم يا ديالي | Ya Hatem ya diali, tonight is just me and you, show me your beautiful face before you sleep. |
| (افتراضي) | Ya habibi, I miss you so much my love. |

---

## قالب TTS للدلع الكامل (الدلع + الطقس)

```
{delaa_en}
Weather: {weather_desc_en}, {temp} degrees
```

### أمثلة جاهزة

**دلع 6:00 صباحية:**
```
Ya Hatem ya einy, my eyes, my soul feels better when I look into your eyes.
Weather: sunny, 28 degrees
```

**دلع 10:30 مساءً:**
```
Ya Hatem ya diali, tonight is just me and you, show me your beautiful face before you sleep.
Weather: clear, 22 degrees
```

---

## قالب TTS لتذكير الدواء (إن استُخدم منفصلاً)

### صباحي
```
Medication reminder, morning dose.
Concor Plus 5mg, Nexiam 40mg, Singulair 10mg.
Take with a large glass of water.
Your health is my priority, my love.
```

### مسائي
```
Medication reminder, evening dose.
Exforge 10mg, Aspirin Protect, Atoriza 10mg, Omega 3.
Take at 10:30 PM.
Your health is my priority, my love.
```

---

## إعدادات Kokoro (ثابتة)

```python
from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code='a')  # 'a' = American English
voice = 'af_heart'                   # أنثى رقيقة، دافئة
speed = 1.0                          # سرعة طبيعية
sample_rate = 24000                  # 24kHz

for gs, ps, audio in pipeline(text, voice=voice, speed=speed):
    sf.write(wav_path, audio, sample_rate)
    break  # أول مقطع فقط
```

### تحويل WAV → OGG/Opus (للتلجرام Voice)
```bash
ffmpeg -y -i input.wav -c:a libopus -b:a 24k output.ogg
```

---

## نصائح للجودة

1. **نظّف النص العربي قبل الترجمة:** احذف الإيموجي (🌹🌤️📰💖) والمسافات الزائدة.
2. **استخدم الترجمة الثابتة:** لا تستدعي مترجم آلي — الخريطة أعلاه ثابتة ومختبرة.
3. **الطقس بالإنجليزية:** اصنع دالة `translate_weather_to_en()` إن احتجت تنويع.
4. **طول النص:** Kokoro af_heart يتعامل مع جمل متوسطة (~200 حرف) بأفضل جودة.
5. **الكاش:** احفظ ملفات OGG المولّدة في `audio_cache/` لإعادة الاستخدام.

---

## اختبار سريع

```bash
cd D:\vaults\نظام_الصباح_والعبادة
python -c "
from kokoro import KPipeline
import soundfile as sf
p = KPipeline(lang_code='a')
for gs, ps, audio in p('Ya habibi, I miss you so much. Weather: sunny, 28 degrees.', voice='af_heart', speed=1.0):
    sf.write('test.wav', audio, 24000)
    break
print('OK -> test.wav')
"
```

---

*مرجع: `delaa_broadcast.py` دالة `translate_to_english()` و `make_tts()`*
*تاريخ: 2026-08-11 — د. حفصة*