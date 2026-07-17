#!/usr/bin/env python3
"""
daily_routine.py — يبني جدول اليوم (صلاة + قرآن + اسم من أسماء الله الحسنى
+ كتابة الرواية + مكالمة الأسرة + أذكار حصن المسلم) ويحطه في ملاحظة اليوم بالخزنة.

الإعداد: ~/.hermes/config/routine.toml
التشغيل: python3 daily_routine.py
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import tomllib
except ImportError:
    sys.exit("احتاج مكتبة tomllib (Python 3.11+ أو pip install tomli)")

try:
    import requests
except ImportError:
    sys.exit("احتاج مكتبة requests: pip install requests --break-system-packages")

CONFIG_PATH = Path.home() / ".hermes" / "config" / "routine.toml"

ASMA_AL_HUSNA = [
    ("الرحمن", "ذو الرحمة الواسعة التي تشمل كل شيء"),
    ("الرحيم", "الرحيم بعباده المؤمنين خاصة"),
    ("الملك", "المالك لكل شيء المتصرف فيه"),
    ("القدوس", "المنزه عن كل نقص وعيب"),
    ("السلام", "السالم من كل آفة، مصدر السلامة"),
    ("المؤمن", "المصدق لأنبيائه، المؤمّن لعباده من الخوف"),
    ("المهيمن", "الرقيب الحافظ على كل شيء"),
    ("العزيز", "الغالب الذي لا يُقهر"),
    ("الجبار", "الذي يجبر الضعف ويقهر الجميع بعزته"),
    ("المتكبر", "المتعالي عن صفات الخلق"),
    ("الخالق", "الذي أوجد الأشياء من العدم"),
    ("البارئ", "الذي خلق الخلق بلا تفاوت"),
    ("المصور", "الذي صوّر مخلوقاته فأحسن صورها"),
    ("الغفار", "كثير المغفرة لذنوب عباده"),
    ("القهار", "الغالب لكل شيء القاهر له"),
    ("الوهاب", "كثير العطاء بلا مقابل"),
    ("الرزاق", "الذي يرزق جميع خلقه"),
    ("الفتاح", "الذي يفتح أبواب الرزق والرحمة والحكم بين عباده"),
    ("العليم", "المحيط علمه بكل شيء"),
    ("القابض", "الذي يقبض الأرزاق والأرواح بحكمته"),
    ("الباسط", "الذي يبسط الرزق لمن يشاء"),
    ("الخافض", "الذي يخفض الجبارين والمتكبرين"),
    ("الرافع", "الذي يرفع أولياءه ويعز من يشاء"),
    ("المعز", "الذي يعطي العزة لمن يشاء"),
    ("المذل", "الذي يذل من يشاء بعدله"),
    ("السميع", "الذي يسمع كل صوت"),
    ("البصير", "الذي يرى كل شيء دقيقه وجليله"),
    ("الحكم", "الذي يفصل بين الخلق بحكمه"),
    ("العدل", "الذي لا يجور، المنزه عن الظلم"),
    ("اللطيف", "الرفيق بعباده العالم بدقائق أمورهم"),
    ("الخبير", "العالم ببواطن الأمور وحقائقها"),
    ("الحليم", "الذي لا يعجل بالعقوبة مع قدرته"),
    ("العظيم", "الذي جل قدره عن الإحاطة"),
    ("الغفور", "الساتر للذنوب مع كثرة عفوه"),
    ("الشكور", "الذي يجازي على القليل من الطاعة بالكثير من الثواب"),
    ("العلي", "المتعالي عن صفات الخلق في ذاته وقدره"),
    ("الكبير", "الأعظم من كل شيء"),
    ("الحفيظ", "الذي يحفظ خلقه ويحفظ عليهم أعمالهم"),
    ("المقيت", "المقتدر، وقيل الذي يعطي الأقوات"),
    ("الحسيب", "الكافي عباده، المحاسب لهم على أعمالهم"),
    ("الجليل", "الموصوف بنعوت العظمة والكبرياء"),
    ("الكريم", "كثير الخير، الجواد المعطي بلا حساب"),
    ("الرقيب", "المطلع الذي لا يغيب عنه شيء"),
    ("المجيب", "الذي يجيب دعوة الداعي إذا دعاه"),
    ("الواسع", "الذي وسع كل شيء رحمة وعلماً"),
    ("الحكيم", "الذي يضع كل شيء في موضعه"),
    ("الودود", "المحب لعباده الصالحين المحبوب في قلوبهم"),
    ("المجيد", "العظيم الكريم الواسع الفضل"),
    ("الباعث", "الذي يبعث الخلق يوم القيامة"),
    ("الشهيد", "الذي لا يغيب عنه شيء، الحاضر في كل مكان بعلمه"),
    ("الحق", "الثابت الذي لا يزول، المتحقق وجوده"),
    ("الوكيل", "الذي يتولى أمور عباده ويكفيهم"),
    ("القوي", "الكامل القدرة الذي لا يعجزه شيء"),
    ("المتين", "الشديد القوة الذي لا تنقصه الأعمال"),
    ("الولي", "الناصر لعباده المؤمنين المتولي لأمورهم"),
    ("الحميد", "المحمود في كل أفعاله وأقواله"),
    ("المحصي", "الذي أحصى كل شيء علماً وعداً"),
    ("المبدئ", "الذي بدأ الخلق من العدم"),
    ("المعيد", "الذي يعيد الخلق بعد الموت"),
    ("المحيي", "الذي يهب الحياة"),
    ("المميت", "الذي يقدّر الموت على كل حي"),
    ("الحي", "الباقي الذي لا يموت"),
    ("القيوم", "القائم بذاته المقيم لغيره"),
    ("الواجد", "الغني الذي لا يفتقر لشيء"),
    ("الماجد", "الواسع الكرم والفضل"),
    ("الواحد", "المتفرد بذاته وصفاته وأفعاله"),
    ("الصمد", "الذي يُقصد في الحوائج، الذي لا يحتاج لغيره"),
    ("القادر", "الذي لا يعجزه شيء"),
    ("المقتدر", "كامل القدرة النافذ الإرادة"),
    ("المقدم", "الذي يقدم من يشاء بفضله"),
    ("المؤخر", "الذي يؤخر من يشاء بحكمته"),
    ("الأول", "الذي ليس قبله شيء"),
    ("الآخر", "الذي ليس بعده شيء"),
    ("الظاهر", "الذي دلت عليه جميع الدلائل"),
    ("الباطن", "الذي احتجب عن إدراك الأبصار والأوهام"),
    ("الوالي", "المالك لجميع الأمور المتصرف فيها"),
    ("المتعالي", "المنزه عن صفات الخلق"),
    ("البر", "المحسن إلى خلقه اللطيف بهم"),
    ("التواب", "الذي يعود على عباده بالمغفرة كلما تابوا"),
    ("المنتقم", "الذي ينتقم من العصاة بعدله"),
    ("العفو", "الذي يمحو السيئات ويتجاوز عنها"),
    ("الرؤوف", "شديد الرحمة بعباده"),
    ("مالك الملك", "المتصرف في الملك كله بلا منازع"),
    ("ذو الجلال والإكرام", "المستحق للتعظيم والإكرام"),
    ("المقسط", "العادل في حكمه"),
    ("الجامع", "الذي يجمع الخلائق ليوم لا ريب فيه"),
    ("الغني", "الذي لا يحتاج إلى أحد"),
    ("المغني", "الذي يغني من يشاء من عباده"),
    ("المانع", "الذي يمنع أسباب البلاء عن أوليائه"),
    ("الضار", "الذي يقدّر الضر بحكمته"),
    ("النافع", "الذي يقدّر النفع لمن يشاء"),
    ("النور", "الذي نوّر السماوات والأرض بنوره وهداه"),
    ("الهادي", "الذي يهدي عباده إلى الحق"),
    ("البديع", "الذي أبدع الخلق على غير مثال سابق"),
    ("الباقي", "الدائم الذي لا يفنى"),
    ("الوارث", "الباقي بعد فناء خلقه، الذي يرث الأرض ومن عليها"),
    ("الرشيد", "الهادي إلى سبيل الرشاد"),
    ("الصبور", "الذي لا يعاجل العصاة بالعقوبة"),
]

WAKE_UP_ADHKAR = [
    "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ",
    "اللَّهُمَّ لَكَ الْحَمْدُ أَنْتَ أَحْيَيْتَنَا، لَكَ الْحَمْدُ أَنْتَ أَمَاتَّنَا، لَكَ الْحَمْدُ أَنْتَ تُبْعَثُنَا",
]

MORNING_ADHKAR = [
    "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ",
    "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ... (سيد الاستغفار)",
    "سُبْحَانَ اللهِ وَبِحَمْدِهِ" + " × 100",
    "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ..." + " × 10",
    "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ" + " × 100",
]

EVENING_ADHKAR = [
    "اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ",
    "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ... (سيد الاستغفار)",
    "سُبْحَانَ اللهِ وَبِحَمْدِهِ" + " × 100",
    "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ..." + " × 10",
    "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ" + " × 100",
]

SLEEP_ADHKAR = [
    "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
    "آيَةُ الْكُرْسِيِّ (آمَنَ الرَّسُولُ بِمَا أُنْزِلَ إِلَيْهِ مِنْ رَبِّهِ...)",
    "الْمَعَوِّذَتَانِ: الفَلَق + النَّاس + الإِخْلَاص",
    "اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ",
]

DUAS = [
    "اللهم اجعل هذا اليوم عوناً لي على طاعتك وذكرك",
    "رب اشرح لي صدري ويسر لي أمري",
    "اللهم بارك لي في وقتي واجعله شاهداً لي لا علي",
    "اللهم ألهمني رشدي وأعذني من شر نفسي",
    "رب زدني علماً وارزقني الإخلاص في القول والعمل",
    "اللهم اجعل القرآن ربيع قلبي ونور صدري",
    "اللهم اجمع بيني وبين أهلي على الخير والمودة",
    "اللهم اجعل خير عملي خواتمه وخير أيامي يوم ألقاك فيه",
    "رب اجعلني مقيم الصلاة ومن ذريتي",
    "اللهم انفعني بما علمتني وعلمني ما ينفعني",
]


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        sys.exit(f"مفيش ملف إعدادات في {CONFIG_PATH}. انسخ routine.toml هناك الأول.")
    with open(CONFIG_PATH, "rb") as f:
        return tomllib.load(f)


def fetch_prayer_times(cfg: dict, date: datetime) -> dict:
    """يجيب مواقيت الصلاة من Aladhan API، مع كاش يومي محلي."""
    cache_dir = Path(cfg["cache"]["dir"]).expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"prayer_times_{date:%Y-%m-%d}.json"

    if cache_file.exists():
        return json.loads(cache_file.read_text())["data"]["timings"]

    loc = cfg["location"]
    resp = requests.get(
        "https://api.aladhan.com/v1/timings/" + date.strftime("%d-%m-%Y"),
        params={
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "method": loc["calculation_method"],
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    cache_file.write_text(json.dumps(data, ensure_ascii=False))
    return data["data"]["timings"]


def hhmm(timing: str) -> str:
    return timing[:5]


def add_minutes(t: str, minutes: int) -> str:
    dt = datetime.strptime(t, "%H:%M") + timedelta(minutes=minutes)
    return dt.strftime("%H:%M")


def format_multi(label_title: str, items: list[str]) -> str:
    lines = [label_title]
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines)


def build_schedule(cfg: dict, timings: dict, day_index: int) -> tuple[list[tuple[str, str]], str]:
    s = cfg["schedule"]
    fajr = hhmm(timings["Fajr"])
    dhuhr = hhmm(timings["Dhuhr"])
    asr = hhmm(timings["Asr"])
    maghrib = hhmm(timings["Maghrib"])
    isha = hhmm(timings["Isha"])

    name, meaning = ASMA_AL_HUSNA[day_index % len(ASMA_AL_HUSNA)]
    dua = DUAS[day_index % len(DUAS)]

    quran_start = add_minutes(fajr, s["quran_minutes_after_fajr"])
    quran_end = add_minutes(quran_start, s["quran_duration_minutes"])
    morning_adhkar_time = add_minutes(fajr, s.get("morning_adhkar_minutes_after_fajr", 35))
    asma_time = add_minutes(fajr, s["asma_minutes_after_fajr"])
    writing_start = add_minutes(asr, s["writing_minutes_after_asr"])
    writing_end = add_minutes(writing_start, s["writing_duration_minutes"])
    evening_adhkar_time = add_minutes(maghrib, s.get("evening_adhkar_minutes_after_maghrib", 0))
    call_time = add_minutes(maghrib, s["family_call_minutes_after_maghrib"])
    sleep_adhkar_time = add_minutes(s["sleep_time"], -s.get("sleep_adhkar_minutes_before_sleep", 15))

    rows = [
        (fajr, "صلاة الفجر"),
        (fajr, format_multi("أذكار الاستيقاظ", WAKE_UP_ADHKAR)),
        (quran_start, f"قراءة جزء من القرآن (حتى {quran_end})"),
        (morning_adhkar_time, format_multi("أذكار الصباح", MORNING_ADHKAR)),
        (asma_time, f"اسم اليوم: {name} — {meaning}"),
        (dhuhr, "صلاة الظهر"),
        (asr, "صلاة العصر"),
        (writing_start, f"كتابة / مراجعة الرواية (حتى {writing_end})"),
        (maghrib, "صلاة المغرب"),
        (evening_adhkar_time, format_multi("أذكار المساء", EVENING_ADHKAR)),
        (call_time, "مكالمة الزوجة والوالدة"),
        (isha, "صلاة العشاء"),
        (sleep_adhkar_time, format_multi("أذكار النوم", SLEEP_ADHKAR)),
        (s["sleep_time"], "النوم"),
    ]
    rows.sort(key=lambda r: r[0])
    return rows, dua


def render_markdown(rows: list[tuple[str, str]], dua: str, header: str) -> str:
    lines = [header, "", f"> دعاء اليوم: {dua}", ""]
    for time, label in rows:
        if "\n" in label:
            first_line, rest = label.split("\n", 1)
            lines.append(f"- **{time}** | {first_line}")
            for sub in rest.split("\n"):
                if sub.strip():
                    lines.append(f"  {sub}")
        else:
            lines.append(f"- **{time}** | {label}")
    lines.append("")
    return "\n".join(lines)


def upsert_into_note(vault_path: Path, note_pattern: str, date: datetime,
                      header: str, block: str) -> Path:
    note_path = vault_path / note_pattern.format(date=date.strftime("%Y-%m-%d"))
    note_path.parent.mkdir(parents=True, exist_ok=True)
    content = note_path.read_text(encoding="utf-8") if note_path.exists() else ""
    if header in content:
        print(f"الروتين موجود بالفعل في {note_path}، معملتش تعديل.")
        return note_path
    separator = "\n\n" if content and not content.endswith("\n\n") else ""
    note_path.write_text(content + separator + block, encoding="utf-8")
    return note_path


def main():
    cfg = load_config()
    tz = ZoneInfo(cfg["location"]["timezone"])
    now = datetime.now(tz)
    timings = fetch_prayer_times(cfg, now)
    rows, dua = build_schedule(cfg, timings, now.timetuple().tm_yday)
    header = cfg["vault"]["section_header"]
    block = render_markdown(rows, dua, header)
    vault_path = Path(cfg["vault"]["path"]).expanduser()
    note_path = upsert_into_note(
        vault_path, cfg["vault"]["daily_note_pattern"], now, header, block
    )
    print(f"تم كتابة الروتين في: {note_path}")


if __name__ == "__main__":
    main()
