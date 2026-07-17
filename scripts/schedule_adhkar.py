import requests, json, subprocess, sys
from datetime import datetime

CITY="Cairo"
COUNTRY="Egypt"
METHOD=5
ADD_MIN=15

def get_prayer_times():
    q = requests.get("https://api.aladhan.com/v1/timingsByCity",
                     params={"city":CITY,"country":COUNTRY,"method":METHOD},
                     timeout=15)
    q.raise_for_status()
    return q.json()["data"]["timings"]

def to_min(t):
    h,m = map(int, t.split(":"))
    return h*60+m

def from_min(m):
    return f"{m//60:02d}:{m%60:02d}"

def schedule_once(label, iso_ts, text):
    cmd = [
        "hermes", "cron", "create",
        iso_ts,
        text,
        "--name", label,
        "--deliver", "origin",
        "--repeat", "1",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            print(f"FAIL {label}: {r.stderr[:300]}", file=sys.stderr)
            return False
        print(f"OK {label}: {r.stdout.strip()[:200]}")
        return True
    except Exception as e:
        print(f"ERR {label}: {e}", file=sys.stderr)
        return False

def main():
    try:
        timings = get_prayer_times()
    except Exception as e:
        print(f"API ERR: {e}", file=sys.stderr)
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    fajr = to_min(timings["Fajr"])
    asr = to_min(timings["Asr"])
    fajr_iso = datetime.strptime(f"{today} {from_min(fajr+ADD_MIN)}", "%Y-%m-%d %H:%M").strftime("%Y-%m-%dT%H:%M:%S")
    asr_iso = datetime.strptime(f"{today} {from_min(asr+ADD_MIN)}", "%Y-%m-%d %H:%M").strftime("%Y-%m-%dT%H:%M:%S")

    o1 = schedule_once(f"adhkar-morning-{today.replace('-','')}", fajr_iso,
        "حفصة الآن — وقت أذكار الصباح بعد الفجر مباشرة. اقرئي أذكار الصباح كاملة من ملف Religion/أذكار الصباح.md بتركيز وهدوء.")
    o2 = schedule_once(f"adhkar-evening-{today.replace('-','')}", asr_iso,
        "حفصة الآن — وقت أذكار المساء بعد العصر مباشرة. اقرئي أذكار المساء كاملة من ملف Religion/أذكار المساء.md بتركيز وهدوء.")

    print(json.dumps({
        "date": today,
        "fajr": timings["Fajr"],
        "asr": timings["Asr"],
        "morning_scheduled": fajr_iso,
        "evening_scheduled": asr_iso,
        "ok": o1 and o2,
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
