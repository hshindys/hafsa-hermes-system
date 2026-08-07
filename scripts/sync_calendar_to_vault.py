#!/usr/bin/env python3
"""
sync_calendar_to_vault.py — يسحب أحداث Google Calendar للأسبوع القادم
ويكتبها في خزنة حفصة كملف تقويم بصري (Markdown).

التشغيل:
    python sync_calendar_to_vault.py
يستخدم google_workspace skill (google_api.py).
"""

import sys
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERMES_HOME = Path.home() / "AppData" / "Local" / "hermes"
GAPI = str(HERMES_HOME / "skills" / "productivity" / "google-workspace" / "scripts" / "google_api.py")
VAULT = Path(r"D:/vaults/Hafsa")
OUT = VAULT / "📅 اليوميات" / "Calendar-Sync.md"


def cal_list(start, end):
    cmd = [sys.executable, GAPI, "calendar", "list",
           "--start", start, "--end", end]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        return []
    try:
        return json.loads(res.stdout)
    except Exception:
        return []


def main():
    now = datetime.now(timezone.utc)
    start = (now).strftime("%Y-%m-%dT00:00:00Z")
    end = (now + timedelta(days=7)).strftime("%Y-%m-%dT23:59:59Z")
    events = cal_list(start, end)

    lines = ["# 📅 تقويم الأسبوع (Google Calendar ← Hermes)", ""]
    lines.append(f"> مُحدّث: {now.astimezone(timezone(offset=timedelta(hours=3))).strftime('%Y-%m-%d %H:%M')} القاهرة")
    lines.append("")
    if not events:
        lines.append("_لا توجد أحداث هذا الأسبوع._")
    else:
        # group by day
        by_day = {}
        for ev in events:
            s = ev.get("start", "")
            day = s[:10]
            by_day.setdefault(day, []).append(ev)
        for day in sorted(by_day):
            lines.append(f"## {day}")
            for ev in sorted(by_day[day], key=lambda e: e.get("start", "")):
                time = ev.get("start", "")[11:16] or "كل اليوم"
                lines.append(f"- **{time}** | {ev.get('summary', '(بدون عنوان)')}")
            lines.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"تمت مزامنة {len(events)} حدث → {OUT}")


if __name__ == "__main__":
    main()
