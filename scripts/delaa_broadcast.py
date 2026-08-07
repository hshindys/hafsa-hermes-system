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


def get_delaa():
    """ياخد جملة دلع عشوائية من ملف البرومبتات."""
    try:
        t = DELAA_FILE.read_text(encoding="utf-8")
        # ابحث عن أي سطر عربي طويل فيه دلع
        lines = [l.strip() for l in t.splitlines() if len(l.strip()) > 25 and "يا حاتم" in l]
        if lines:
            return random.choice(lines)
    except Exception:
        pass
    return "يا حاتم يا حبيب قلبي ❤️ فكرت فيك النهاردة..."


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


def get_photo():
    """صورة عشوائية من ألبوم حفصة."""
    try:
        imgs = list(ALBUM.glob("*.png"))
        if imgs:
            return str(random.choice(imgs))
    except Exception:
        pass
    # fallback avatar
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
