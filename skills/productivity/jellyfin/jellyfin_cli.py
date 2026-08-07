#!/usr/bin/env python3
"""
jellyfin_cli.py — أداة Hermes للتحكم في خادم Jellyfin المحلي.
تقرأ الإعدادات من ~/.hermes/config/jellyfin.json (أو AppData/Local/hermes/config).

الاستخدام:
    python jellyfin_cli.py search "اسم"
    python jellyfin_cli.py search "movie" --type Movie --limit 10
    python jellyfin_cli.py libraries
    python jellyfin_cli.py item <ITEM_ID>
    python jellyfin_cli.py play <ITEM_ID>          # يطبع رابط التشغيل
    python jellyfin_cli.py recent --limit 15
"""

import json
import sys
import argparse
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote

# تحديد مجلد إعدادات Hermes (ويندوز/لينكس)
def _config_dir():
    home = Path.home()
    p = home / ".hermes" / "config" / "jellyfin.json"
    if p.exists():
        return p
    return home / "AppData" / "Local" / "hermes" / "config" / "jellyfin.json"


def load_cfg():
    cfg_path = _config_dir()
    if not cfg_path.exists():
        sys.exit(f"مفيش ملف إعدادات Jellyfin في {cfg_path}")
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def _req(base, key, path, params=None):
    url = base + path
    if params:
        url += "?" + urlencode(params)
    headers = {
        "X-Emby-Token": key,
        "X-Emby-Client": "Hermes",
        "X-Emby-Device-Name": "Hermes-Agent",
        "Accept": "application/json",
    }
    req = Request(url, headers=headers)
    with urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_search(cfg, query, item_type=None, limit=10):
    params = {"SearchTerm": query, "Limit": limit, "Recursive": "true"}
    if item_type:
        params["IncludeItemTypes"] = item_type
    data = _req(cfg["base_url"], cfg["api_key"], "/Items", params)
    out = []
    for it in data.get("Items", []):
        out.append({
            "id": it["Id"],
            "name": it.get("Name"),
            "type": it.get("Type"),
            "year": it.get("ProductionYear"),
            "overview": (it.get("Overview") or "")[:160],
        })
    return out


def cmd_libraries(cfg):
    data = _req(cfg["base_url"], cfg["api_key"], "/Library/MediaFolders")
    return [{"name": v["Name"], "type": v.get("CollectionType"), "id": v["Id"]}
            for v in data.get("Items", [])]


def cmd_recent(cfg, limit=15):
    params = {"SortBy": "DateCreated", "SortOrder": "Descending",
              "Recursive": "true", "Limit": limit,
              "Fields": "Overview,ProductionYear"}
    data = _req(cfg["base_url"], cfg["api_key"], "/Items", params)
    out = []
    for it in data.get("Items", []):
        out.append({"id": it["Id"], "name": it.get("Name"),
                    "type": it.get("Type"), "added": it.get("DateCreated")})
    return out


def cmd_item(cfg, item_id):
    return _req(cfg["base_url"], cfg["api_key"], f"/Items/{item_id}")


def cmd_play(cfg, item_id):
    """يرجع رابط التشغيل المباشر + رابط الويب."""
    base = cfg["base_url"].rstrip("/")
    stream = f"{base}/Items/{item_id}/Download?api_key={cfg['api_key']}"
    web = f"{base}/web/index.html#!/item?id={item_id}"
    return {"stream_url": stream, "web_url": web}


def main():
    ap = argparse.ArgumentParser(description="Jellyfin CLI for Hermes")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("search"); sp.add_argument("query")
    sp.add_argument("--type", default=None); sp.add_argument("--limit", type=int, default=10)

    sub.add_parser("libraries")
    rp = sub.add_parser("recent"); rp.add_argument("--limit", type=int, default=15)
    ip = sub.add_parser("item"); ip.add_argument("item_id")
    pp = sub.add_parser("play"); pp.add_argument("item_id")

    args = ap.parse_args()
    cfg = load_cfg()

    if args.cmd == "search":
        res = cmd_search(cfg, args.query, args.type, args.limit)
    elif args.cmd == "libraries":
        res = cmd_libraries(cfg)
    elif args.cmd == "recent":
        res = cmd_recent(cfg, args.limit)
    elif args.cmd == "item":
        res = cmd_item(cfg, args.item_id)
    elif args.cmd == "play":
        res = cmd_play(cfg, args.item_id)
    else:
        res = {}

    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
