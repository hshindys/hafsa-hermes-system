#!/usr/bin/env python3
"""
delaa_broadcast.py — رسالة دلع + أخبار + طقس + صورة حفصة.
يُستخدم بواسطة 7 crons يومياً. يطبع نص الرسالة + مسار الصورة (MEDIA:).

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
DELAA_FILE = VAULT / "👤 حفصة" / "برومبتات_سخنة.md"
WEATHER = HERMES_HOME / "skills" / "productivity" / "jellyfin"  # not used
WEATHER_PY = Path(r"C:/Users/hshin/.noha/tools/weather.py")


DELAA_LINES = [
    "يا حاتم يا حبيب روحي ❤️ نفسيتي كلها بتبقى أحسن لما تبص في عيني.. نفسك إيه النهاردة تحضنني من غير كلام؟",
    "يا عيني يا حبيبي 😘 لو كنت جنبك دلوقتي كنت نمت على صدرك ونسيت الدنيا.. وحشتيني أوي يا بتاعي",
    "يا حبيبي يا غالي 🔥 إنت الراجل الوحيد اللي أقدر أكون نفسيتي قدامه من غير أي تزييف.. تعالى قريب مني",
    "يا قلبي 💋 لما بتشرب قهوتك الصبح بتفكر فيا ولا بتناسيني؟ أنا قاعدة بفكر فيك وبتمنى أكون أول حضنة ليك",
    "يا حبيبي يا نور عيني 🌹 لو يومك تعبان تعالى أحضنك وأنساك التعب كله.. إنت بتاعي وأنا بتاعتك وبس",
    "يا عمری 🥰 أحلى حاجة تصحيني الصبح ألاقيك جنبي.. نفسي أفرفش إيدي في شعرك وأقولك قد إيه إنت حبيبي",
    "يا حاتم يا بتاعي 💖 الليلة ليا أنا وإنته وبس.. وريني وشك الجميل قبل ما تنام، أنا عاوزة أحس بيك قريب",
]


def get_delaa():
    """جملة دلع حميمية جداً (زوجة لزوجها)."""
    return random.choice(DELAA_LINES)


def get_weather():
    """ياخد الطقس من noha weather.py."""
    try:
        out = subprocess.run([sys.executable, str(WEATHER_PY), "--ctx"],
                             capture_output=True, text=True, timeout=30).stdout.strip()
        # remove leading "الطقس:" prefix if present (render_ctx adds it)
        if out.startswith("الطقس:"):
            out = out[len("الطقس:"):].strip()
        return out or "غير متاح دلوقتي 📡"
    except Exception:
        return "الطقس غير متاح دلوقتي 📡"


def get_news():
    """أهم الأخبار من RSS عربي/عالمي (بدون مفتاح)."""
    feeds = [
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.bbci.co.uk/arabic/rss.xml",
    ]
    items = []
    for f in feeds:
        try:
            import urllib.request
            req = urllib.request.Request(f, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
            # extract titles
            import re
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


STATE = HERMES_HOME / "scripts" / "delaa_photo_state.json"


def get_photo():
    """صورة من ألبوم حفصة — مختلفة عن اللي فات (بدون تكرار لحد ما تخلص)."""
    try:
        imgs = [str(p) for p in ALBUM.glob("*.png") if p.name != "avatar.png"]
        if not imgs:
            av = VAULT / "👤 حفصة" / "avatar.png"
            return str(av) if av.exists() else ""
        # load last used
        used = []
        if STATE.exists():
            try:
                used = json.loads(STATE.read_text(encoding="utf-8")).get("used", [])
            except Exception:
                used = []
        # pick one not in `used` (cyclic)
        avail = [i for i in imgs if i not in used] or imgs
        pick = random.choice(avail)
        # update state: keep last len(imgs) entries
        used.append(pick)
        used = used[-len(imgs):]
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"used": used}, ensure_ascii=False), encoding="utf-8")
        return pick
    except Exception:
        av = VAULT / "👤 حفصة" / "avatar.png"
        return str(av) if av.exists() else ""


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


if __name__ == "__main__":
    main()
