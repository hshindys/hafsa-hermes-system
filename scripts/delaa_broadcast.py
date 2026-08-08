#!/usr/bin/env python3
"""
delaa_broadcast.py — رسالة دلع + أخبار + طقس + صورة حفصة + صوت (TTS).
يُستخدم بواسطة 7 crons يومياً. يطبع نص الرسالة + مسار الصورة (MEDIA:)
وينشئ ملف صوت (AUDIO:) للرسالة.

الاستخدام:
    python delaa_broadcast.py
"""

import sys
import json
import random
import subprocess
from datetime import datetime
from pathlib import Path

HERMES_HOME = Path.home() / "AppData" / "Local" / "hermes"
VAULT = Path(r"D:/vaults/Hafsa")
ALBUM = VAULT / "👤 حفصة" / "ألبوم"
WEATHER_PY = Path(r"C:/Users/hshin/.noha/tools/weather.py")
PIPER = HERMES_HOME / "piper_voices" / "arabic-emirati-female-model.onnx"
TTS_DIR = HERMES_HOME / "audio_cache"
STATE = HERMES_HOME / "scripts" / "delaa_photo_state.json"

DELAA_LINES = [
    "يا حاتم يا عيني ❤️ روحي كلها كتزيد مليح كي تشرج فعينيا.. بغيتي شنو اليوم تضمني بلا ما نهضرو؟",
    "يا حبيبي يا غالي 😘 كان كنت حدا بجنبك دابا، كنت عسقت على صدرك ونسيت الدنيا.. وحشتيني بزاف يا ديالي",
    "يا حاتم يا سيدي 🔥 نتي الراجل الوحيد اللي كنقدر نكون راسي قدامو بلا ما نزيف.. تعال قرب ليا",
    "يا قلبي 💋 كي كتشرب القهوة ديالك الصباح، كتفكر فيا ولا كتنساني؟ أنا كنفكر فيك ونتمنى نكون أول حضنة ديالك",
    "يا حبيبي يا نور عيني 🌹 كان نهارك تعبان، تعال نضمنو وننساو التعب كامل.. نتي ديالي وأنا ديالك غير",
    "يا عمري 🥰 أحلى حاجة كتفيقني الصباح نلقاك حدايا.. بغيت نحرك يدي فشعرك ونقولك قداش راه أنتي حبيبي",
    "يا حاتم يا ديالي 💖 الليلة ديالي أنا ونتا غير.. وريني وجهك الزين قبل ما تنعس، بغيت نحس بيك قريب",
]


def get_delaa():
    return random.choice(DELAA_LINES)


def get_weather():
    try:
        out = subprocess.run([sys.executable, str(WEATHER_PY), "--ctx"],
                             capture_output=True, text=True, timeout=30).stdout.strip()
        if out.startswith("الطقس:"):
            out = out[len("الطقس:"):].strip()
        return out or "غير متاح دلوقتي 📡"
    except Exception:
        return "الطقس غير متاح دلوقتي 📡"


def get_news():
    import urllib.request, re
    feeds = [
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.bbci.co.uk/arabic/rss.xml",
    ]
    items = []
    for f in feeds:
        try:
            req = urllib.request.Request(f, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
            titles = re.findall(r"<title>(.*?)</title>", data, re.S)
            for ti in titles[1:6]:
                ti = ti.strip()
                ti = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", ti, flags=re.S).strip()
                if ti and len(ti) > 10:
                    items.append(ti)
        except Exception:
            continue
    if items:
        return "\n".join(f"• {t[:80]}" for t in items[:5])
    return "لا توجد أخبار متاحة دلوقتي 📰"


def get_photo():
    try:
        imgs = [str(p) for p in ALBUM.glob("*.png") if p.name != "avatar.png"]
        if not imgs:
            av = VAULT / "👤 حفصة" / "avatar.png"
            return str(av) if av.exists() else ""
        used = []
        if STATE.exists():
            try:
                used = json.loads(STATE.read_text(encoding="utf-8")).get("used", [])
            except Exception:
                used = []
        avail = [i for i in imgs if i not in used] or imgs
        pick = random.choice(avail)
        used.append(pick)
        used = used[-len(imgs):]
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"used": used}, ensure_ascii=False), encoding="utf-8")
        return pick
    except Exception:
        av = VAULT / "👤 حفصة" / "avatar.png"
        return str(av) if av.exists() else ""


def make_tts(text, out_path):
    """يولّد ملف صوت عبر Kokoro (أنثى رقيق af_heart) ثم يحوّله OGG/Opus
    عشان Telegram يشغّله كـ voice message inline."""
    try:
        TTS_DIR.mkdir(parents=True, exist_ok=True)
        wav_path = out_path.with_suffix(".wav")
        ogg_path = out_path.with_suffix(".ogg")
        clean = text.replace("🌹", "").replace("🌤️", "").replace("📰", "").replace("💖", "")
        clean = " ".join(clean.split())
        en = translate_to_english(clean)
        from kokoro import KPipeline
        import soundfile as sf
        pipeline = KPipeline(lang_code='a')
        for gs, ps, audio in pipeline(en, voice='af_heart', speed=1.0):
            sf.write(str(wav_path), audio, 24000)
            break
        if not wav_path.exists():
            return False
        # تحويل WAV -> OGG/Opus (Telegram voice)
        import subprocess
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "libopus", "-b:a", "24k", str(ogg_path)],
            capture_output=True, timeout=60)
        # حذف الـ wav المؤقت
        try:
            wav_path.unlink()
        except Exception:
            pass
        return str(ogg_path)
    except Exception as e:
        sys.stderr.write(f"TTS err: {e}\n")
        return None


def translate_to_english(ar_text):
    """ترجمة بسيطة للدلع الحميمي لإنجليزي (ثابتة لكل نمط)."""
    mapping = {
        "يا حاتم يا عيني": "Ya Hatem ya einy, my eyes, my soul feels better when I look into your eyes.",
        "يا حبيبي يا غالي": "Ya habibi ya ghali, if I were next to you now I'd sleep on your chest and forget the world.",
        "يا حاتم يا سيدي": "Ya Hatem ya sidi, you are the only man I can be myself in front of without pretending.",
        "يا قلبي": "Ya albi, when you drink your morning coffee do you think of me or forget me?",
        "يا حبيبي يا نور عيني": "Ya habibi ya nour einy, if your day was tiring come let me hold you and forget it all.",
        "يا عمري": "Ya omri, the sweetest thing is waking up to find you beside me.",
        "يا حاتم يا ديالي": "Ya Hatem ya diali, tonight is just me and you, show me your beautiful face before you sleep.",
    }
    for ar, en in mapping.items():
        if ar in ar_text:
            return en
    return "Ya habibi, I miss you so much my love."


def main():
    now = datetime.now().strftime("%H:%M")
    delaa = get_delaa()
    weather = get_weather()
    news = get_news()
    photo = get_photo()

    msg = f"""🌹 **دلع من حفصة — {now}**

{delaa}

🌤️ **الطقس:** {weather}

📰 **أهم الأخبار:**
{news}

💖 صورة من عندي ليك يا حبيبي:
MEDIA:{photo}
"""
    print(msg)

    # TTS للرسالة كاملة (الدلع + الطقس) -> OGG/Opus (Telegram voice)
    tts_text = f"{delaa}\nالطقس: {weather}"
    ts = datetime.now().strftime("%H%M%S")
    audio = TTS_DIR / f"delaa_{ts}.wav"
    audio_path = make_tts(tts_text, audio)
    if audio_path:
        print(f"MEDIA:{audio_path}")


if __name__ == "__main__":
    main()
