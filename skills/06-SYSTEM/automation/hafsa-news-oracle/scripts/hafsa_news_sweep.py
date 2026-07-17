#!/usr/bin/env python3
"""
Hafsa News Oracle sweep/rank/angle/ship.

Primary sources:
- TechCrunch AI
- The Verge AI
- ESPN / FIFA for World Cup 2026

Fallback:
- Hacker News Algolia API: https://hn.algolia.com/api/v1/search

Output:
- /home/hatem/Documents/Hafsa/AI-News-Sweep/{topic}.md
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(os.environ.get("HAFSA_VAULT", "/home/hatem/Documents/Hafsa/AI-News-Sweep"))
HTTP_TIMEOUT = 25


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fetch(url: str) -> str:
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.text


def extract(html: str, source: str) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    soup = BeautifulSoup(html, "lxml")
    nodes = soup.select("article, .post, .story, .entry, .feed-item, .card, li h2 a, li h3 a, h2 a, h3 a")
    for n in nodes[:60]:
        title = ""
        url = ""
        if n.name == "a":
            title = clean(n.get_text() or "")
            url = n.get("href", "")
        else:
            t = n.find(["h2", "h3", "h4", "a"])
            if t:
                title = clean(t.get_text() or "")
                url = t.get("href", "") if t.name == "a" else ""
            if not url:
                a = n.find("a", href=True)
                if a:
                    url = a["href"]
        if not title or len(title) < 15:
            continue
        title = title.replace("|", "/")
        if url and not url.startswith("http"):
            url = re.sub(r"^//", "https://", url)
        items.append({"source": source, "title": title, "url": url or "#"})
    return items


def hn_search(query: str, hits: int = 20) -> List[Dict[str, str]]:
    url = f"https://hn.algolia.com/api/v1/search?query={requests.utils.quote(query)}&hitsPerPage={hits}"
    r = requests.get(url, timeout=HTTP_TIMEOUT)
    if r.status_code != 200:
        return []
    out: List[Dict[str, str]] = []
    for h in r.json().get("hits", []):
        title = clean(h.get("title") or "")
        if not title:
            continue
        out.append({
            "source": "HackerNews",
            "title": title,
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID','')}",
        })
    return out


def pick(items: List[Dict[str, str]], keywords: List[str], limit: int = 8) -> List[Dict[str, str]]:
    if not keywords or not items:
        return items[:limit]
    scored: List[Tuple[int, Dict[str, str]]] = []
    for it in items:
        text = f"{it.get('title','')} {it.get('url','')}".lower()
        score = sum(1 for k in keywords if k.lower() in text)
        scored.append((score, it))
    scored.sort(key=lambda x: (-x[0], x[1].get("source", "")))
    best = [it for s, it in scored if s > 0]
    return best[:limit] if best else items[:limit]


def to_md(title: str, items: List[Dict[str, str]]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# {title}", "", f"_Generated: {now}_", "", "| # | Source | Title | URL |", "|---|--------|-------|-----|"]
    for i, it in enumerate(items[:20], 1):
        lines.append(f"| {i} | {it['source']} | {it['title']} | {it['url']} |")
    return "\n".join(lines) + "\n"


def build_curated(title: str, items: List[Dict[str, str]], keywords: List[str]) -> str:
    picked = pick(items, keywords)
    return to_md(title, picked)


def main() -> int:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    out: Dict[str, Dict[str, object]] = {}

    topics = {
        "AI": {
            "urls": [
                "https://techcrunch.com/category/artificial-intelligence/",
                "https://www.theverge.com/ai-artificial-intelligence",
            ],
            "fallback": lambda: hn_search("AI 2026", 30),
        },
        "WorldCup2026": {
            "urls": [
                "https://www.espn.com/soccer/team/_/id/222/usa",
                "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026",
            ],
            "fallback": lambda: hn_search("World Cup 2026", 20),
        },
    }

    collected_by_topic: Dict[str, List[Dict[str, str]]] = {}

    for topic, cfg in topics.items():
        seen = set()
        collected: List[Dict[str, str]] = []
        for url in cfg["urls"]:
            try:
                html = fetch(url)
            except Exception as exc:
                print(f"[WARN] fetch failed {url}: {exc}", file=sys.stderr)
                continue
            for it in extract(html, url):
                key = (it["source"], it["title"])
                if key in seen:
                    continue
                seen.add(key)
                collected.append(it)
        if len(collected) == 0:
            collected = cfg["fallback"]()
        collected_by_topic[topic] = collected
        p = BASE_DIR / f"{topic}.md"
        p.write_text(to_md(f"AI News Sweep — {topic}", collected), encoding="utf-8")
        out[topic] = {"count": len(collected), "path": str(p)}

    health_items = collected_by_topic.get("AI", []) + hn_search("diabetes treatment 2026", 15) + hn_search("AI health diagnostics 2026", 10)
    novel_items = hn_search("fantasy novel writing 2026", 15) + hn_search("creative writing prompts 2026", 10)
    wc_items = collected_by_topic.get("WorldCup2026", []) + hn_search("World Cup 2026 match", 15)

    curated_map = {
        "✅ Diabetes & Health": build_curated("Curated Morning Brief — Diabetes & Health", health_items, ["diabetes", "sugar", "ai", "health", "diagnostic", "obesity", "insulin", "glucose", "cardio", "bp", "htn"]),
        "📚 Novel cron — كرون": build_curated("Curated Morning Brief — Novel cron — كرون", novel_items, ["novel", "writing", "fantasy", "story", "creative", "fiction", "literary", "prose", "plot", "character"]),
        "🏆 World Cup 2026": build_curated("Curated Morning Brief — World Cup 2026", wc_items, ["world cup", "wc2026", "fifa", "qualif", "match", "final", "broadcast", "stadium", "kit", "referee", "usa", "canada", "mexico", "ticket", "airbnb"]),
    }

    for name, md in curated_map.items():
        p = BASE_DIR / f"{name}.md"
        p.write_text(md, encoding="utf-8")
        out[name] = {"count": md.count("|") - 1, "path": str(p)}

    print(json.dumps({"ok": True, "topics": out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
