#!/usr/bin/env python3
"""novel_context_builder.py — يجمع سياق الكتّابة من story-bible."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIBLE = ROOT / "story-bible"


def read(rel: str) -> str:
    p = BIBLE / rel
    if not p.exists():
        return f"[missing: {rel}]"
    return p.read_text(encoding="utf-8").strip()


def build_context(pov: str, scene_goal: str, present: list[str] | None = None) -> str:
    present = present or []
    jinn_rules = read("jinn-rules.md")
    plot = read("plot-outline.md")
    continuity = read("continuity-log.md")
    style = read("style-guide.md")
    pov_sheet = read(f"characters/{pov}.md") if (BIBLE / "characters" / f"{pov}.md").exists() else "[no pov file]"
    others = "\n\n".join(
        f"### {c}\n{read(f'characters/{c}.md')}" for c in present if c != pov and (BIBLE / "characters" / f"{c}.md").exists()
    )
    return f"""=== JINN RULES ===
{jinn_rules}

=== STYLE GUIDE ===
{style}

=== PLOT OUTLINE ===
{plot}

=== CONTINUITY LOG ===
{continuity}

=== POV: {pov} ===
{pov_sheet}

=== OTHER CHARACTERS ===
{others or 'None'}

=== SCENE GOAL ===
{scene_goal}
"""


if __name__ == "__main__":
    print(build_context("كرون", "لقاء نورك في جزيرة الحكمة لأول مرة", ["نومن", "مشكال"]))
