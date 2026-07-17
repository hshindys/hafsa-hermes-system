from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import requests
except ImportError:
    requests = None

VAULT_DIR = Path("/home/hatem/Documents/Hafsa/AI-News-Sweep")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fetch_url(url: str, timeout: int = 20) -> str:
    if requests is None:
        raise RuntimeError("requests not installed")
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def extract_items_from_html(html: str, source: str) -> List[dict]:
    items: List[dict] = []
    if BeautifulSoup is None:
        return items
    soup = BeautifulSoup(html, "html.parser")
    candidates = soup.select("article, .post, .entry, .story, .feed-item, .card, li h2 a, li h3 a")
    for node in candidates[:20]:
        title = ""
        link = ""
        if node.name == "a":
            title = clean_text(node.get_text() or "")
            link = node.get("href", "")
        else:
            title_node = node.find(["h2", "h3", "h4", "a"])
            if title_node:
                title = clean_text(title_node.get_text() or "")
                link = title_node.get("href", "") if title_node.name == "a" else ""
            if not link:
                a = node.find("a", href=True)
                if a:
                    link = a["href"]
        title = title.replace("\n", " ").strip()
        if not title:
            continue
        if link and not link.startswith("http"):
            link = re.sub(r"^//", "https://", link)
        items.append({"source": source, "title": title, "url": link, "ts": datetime.now(timezone.utc).isoformat()})
    return items


def make_cron_ready_markdown(items: List[dict], topic: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# AI News Sweep — {topic}",
        "",
        f"_Generated: {now}_",
        "",
        "| # | Source | Title | URL |",
        "|---|--------|-------|-----|",
    ]
    for idx, item in enumerate(items[:25], start=1):
        title = item.get("title", "").replace("|", "\\|")
        url = item.get("url", "#")
        source = item.get("source", topic)
        lines.append(f"| {idx} | {source} | {title} | {url} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    targets = {
        "AI": [
            "https://techcrunch.com/category/artificial-intelligence/",
            "https://www.theverge.com/ai-artificial-intelligence",
            "https://www.36kr.com/information/AI/",
        ],
        "WorldCup2026": [
            "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026",
            "https://www.goal.com/en-us/world-cup",
            "https://www.espn.com/soccer/team/_/id/222/usa",
        ],
    }
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    all_outputs = {}
    for topic, urls in targets.items():
        collected: List[dict] = []
        seen = set()
        for url in urls:
            try:
                html = fetch_url(url)
            except Exception as exc:
                print(f"[WARN] fetch failed {url}: {exc}", file=sys.stderr)
                continue
            items = extract_items_from_html(html, url)
            for item in items:
                key = (item["source"], item["title"])
                if key in seen:
                    continue
                seen.add(key)
                collected.append(item)
        md = make_cron_ready_markdown(collected, topic)
        (VAULT_DIR / f"{topic}.md").write_text(md, encoding="utf-8")
        all_outputs[topic] = {"items": len(collected), "path": str(VAULT_DIR / f"{topic}.md")}
    print(json.dumps({"ok": True, "topics": all_outputs}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
