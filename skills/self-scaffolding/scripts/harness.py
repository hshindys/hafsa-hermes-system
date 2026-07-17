#!/usr/bin/env python3
"""
Dynamic harness generator inspired by Ornith 1.0 self-scaffolding.
Generates simple task-specific harnesses on the fly.
"""

import os
import sys
import json
import textwrap
from pathlib import Path

HARNESS_DIR = Path("/tmp/harnesses")
HARNESS_DIR.mkdir(parents=True, exist_ok=True)


def generate_harness(task_description: str) -> dict:
    """Generate a simple Python harness for the given task."""
    
    task_lower = task_description.lower()
    
    if "weather" in task_lower or "طقس" in task_lower:
        return _weather_harness()
    elif "news" in task_lower or "أخبار" in task_lower:
        return _news_harness()
    elif "translate" in task_lower or "ترجمة" in task_lower:
        return _translate_harness()
    else:
        return _generic_harness(task_description)


def _weather_harness() -> dict:
    code = textwrap.dedent('''
        import requests
    
        def run(city: str = "Cairo", days: int = 3) -> dict:
            """Get weather forecast using Open-Meteo (no API key needed)."""
            geo = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1}
            ).json()
            
            if not geo.get("results"):
                return {"error": f"City not found: {city}"}
            
            lat, lon = geo["results"][0]["latitude"], geo["results"][0]["longitude"]
            
            weather = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat, "longitude": lon,
                    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
                    "timezone": "auto",
                    "forecast_days": days
                }
            ).json()
            
            return {"city": city, "forecast": weather.get("daily", {})}
        
        def validate():
            result = run("Cairo", 1)
            return "forecast" in result and result.get("forecast")
    ''')
    
    return {
        "name": "weather_harness",
        "code": code,
        "entry_point": "run",
        "language": "python",
        "config": {"api": "open-meteo", "auth": "none"}
    }


def _news_harness() -> dict:
    code = textwrap.dedent('''
        import requests
        import xml.etree.ElementTree as ET
    
        def run(sources: list = None, max_items: int = 5) -> dict:
            """Fetch latest news from RSS feeds."""
            if sources is None:
                sources = [
                    "https://feeds.bbci.co.uk/news/rss.xml",
                    "https://rss.cnn.com/rss/edition.rss",
                ]
            
            articles = []
            for url in sources[:max_items]:
                try:
                    resp = requests.get(url, timeout=10)
                    root = ET.fromstring(resp.content)
                    for item in root.findall(".//item")[:3]:
                        articles.append({
                            "title": item.find("title").text,
                            "link": item.find("link").text,
                            "published": item.find("pubDate").text,
                        })
                except Exception as e:
                    articles.append({"error": str(e), "source": url})
            
            return {"articles": articles[:max_items], "sources": sources}
        
        def validate():
            result = run(max_items=1)
            return "articles" in result
    ''')
    
    return {
        "name": "news_harness",
        "code": code,
        "entry_point": "run",
        "language": "python",
        "config": {"type": "rss", "auth": "none"}
    }


def _translate_harness() -> dict:
    code = textwrap.dedent('''
        def run(text: str, source_lang: str = "auto", target_lang: str = "ar") -> dict:
            """Simple translation scaffold (placeholder for actual API)."""
            return {
                "original": text,
                "translated": f"[ترجمة] {text}",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "note": "ضع هنا API الترجمة الفعلي"
            }
        
        def validate():
            result = run("Hello", target_lang="ar")
            return "translated" in result
    ''')
    
    return {
        "name": "translate_harness",
        "code": code,
        "entry_point": "run",
        "language": "python",
        "config": {"type": "translation"}
    }


def _generic_harness(task_description: str) -> dict:
    safe_name = "generic_" + "".join(c if c.isalnum() else "_" for c in task_description.lower())[:20]
    
    code = textwrap.dedent(f'''
        def run(*args, **kwargs):
            """Harness for: {task_description}"""
            return {{
                "task": {json.dumps(task_description)},
                "status": "placeholder",
                "args": args,
                "kwargs": kwargs,
                "note": "نفذ هنا المنطق المحدد لهذه المهمة"
            }}
        
        def validate():
            return True
    ''')
    
    return {
        "name": safe_name,
        "code": code,
        "entry_point": "run",
        "language": "python",
        "config": {"type": "generic", "task": task_description}
    }


def save_harness(harness: dict) -> Path:
    """Save harness to /tmp/harnesses/ and return path."""
    name = harness["name"]
    path = HARNESS_DIR / f"{name}.py"
    path.write_text(harness["code"])
    return path


def main():
    if len(sys.argv) < 2:
        print("Usage: harness.py <task_description>")
        sys.exit(1)
    
    task = sys.argv[1]
    harness = generate_harness(task)
    path = save_harness(harness)
    
    print(f"[+] Harness generated: {path}")
    print(f"[+] Name: {harness['name']}")
    print(f"[+] Entry: {harness['entry_point']}()")
    print(json.dumps(harness["config"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
