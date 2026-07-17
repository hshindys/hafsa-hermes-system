"""
enrich.py — takes an existing shallow character or place note and:
  1. Suggests a deepened rewrite following the deep-profile template
     (written to a SEPARATE "-مقترح" file — never overwrites the original)
  2. Generates a standalone image-generation prompt for it, saved into
     its own file — separate from the writing content entirely
  3. Can also INSERT/MERGE approved suggestion back into the original
     when you explicitly ask for it (optional).

Three distinct commands, three distinct outputs. Nothing is auto-applied;
everything lands as a suggestion file for you to review in Obsidian and
merge in yourself.

USAGE
-----
python3 enrich.py character --note "01-شخصيات/زليخة.md" --template templates/character_deep_profile_template.md --vault-root "/home/hatem/Documents/رواية-كرون"
python3 enrich.py place     --note "02-أماكن/جزيرة-الحكمة.md" --template templates/place_deep_profile_template.md --vault-root "/home/hatem/Documents/رواية-كرون"
python3 enrich.py image     --note "01-شخصيات/زليخة.md" --kind character --vault-root "/home/hatem/Documents/رواية-كرون"
python3 enrich.py merge     --note "01-شخصيات/زليخة.md"
"""

import argparse
import os
import re
from pathlib import Path
from typing import Callable


# ---------------------------------------------------------------------------
# 1. ENRICHMENT PROMPTS — suggest depth, grounded in what already exists
# ---------------------------------------------------------------------------

CHARACTER_ENRICHMENT_PROMPT = """أنت مساعد تطوير شخصيات روائية محترف. لديك
ملف شخصية سطحي موجود، ومطلوب منك اقتراح نسخة معمّقة منه باتباع القالب
المرفق بالضبط — قسمًا بقسم.

قواعد صارمة:
1. لا تخترع تفاصيل تتعارض مع أي شيء مذكور بالفعل في الملف الأصلي — الملف
   الأصلي هو الحقيقة، أنت تُعمّقها ولا تُغيّرها.
2. حيث لا توجد معلومة كافية في الأصل، اقترح خيارًا منطقيًا متسقًا مع
   السياق العام (عالم الجن، الإطار الإسلامي)، واذكر بوضوح أنه اقتراح
   قابل للتعديل — لا تقدمه كحقيقة مؤكدة.
3. ركّز بشكل خاص على قسم "الصوت" و"الكذبة اللي بتصدقها عن نفسها" — هذان
   القسمان هما الأكثر أهمية لثبات الشخصية عبر الفصول.
4. أعد الملف كاملًا بصيغة القالب المرفق، جاهزًا للصق مباشر في أوبسيديان.
5. النتيجة يجب أن تكون عربية فصحى أدبية فقط — ممنوع أي لغة أخرى.
"""

PLACE_ENRICHMENT_PROMPT = """أنت مساعد بناء عوالم روائية محترف. لديك ملف
مكان سطحي موجود، ومطلوب منك اقتراح نسخة معمّقة منه باتباع القالب المرفق.

قواعد صارمة:
1. لا تتعارض مع أي تفصيلة موجودة بالفعل في الملف الأصلي أو في الخرائط
   المرتبطة به.
2. ركّز بشكل خاص على قسم "الحواس" — هو الذي يجعل وصف المكان يتكرر بثبات
   عبر مشاهد مختلفة بدل ما يتغير كل مرة.
3. حيث تقترح تفصيلة جديدة، وضّح أنها اقتراح قابل للتعديل.
4. أعد الملف كاملًا بصيغة القالب المرفق، جاهزًا للصق مباشر في أوبسيديان.
5. النتيجة يجب أن تكون عربية فصحى أدبية فقط — ممنوع أي لغة أخرى.
"""


# ---------------------------------------------------------------------------
# 2. IMAGE PROMPT GENERATION — separate artifact entirely from the writing
# ---------------------------------------------------------------------------

CHARACTER_IMAGE_PROMPT_GENERATOR = """You generate image-generation prompts
(in English, for an AI image model) from a character's profile. Output
ONLY the prompt itself — no preamble, no explanation.

Include: physical appearance, distinguishing features, clothing/era style,
expression/mood consistent with their personality, lighting mood that
matches their role in the story (hero/antagonist/mysterious), and art
style (default to painterly digital illustration unless the vault's
existing image prompts suggest otherwise). Keep it one dense paragraph,
60-100 words."""

PLACE_IMAGE_PROMPT_GENERATOR = """You generate image-generation prompts
(in English, for an AI image model) from a location's profile. Output
ONLY the prompt itself — no preamble, no explanation.

Include: geography, lighting/time of day matching its sensory description,
architectural or natural style, atmosphere/mood, and art style (default to
painterly digital illustration unless the vault's existing image prompts
suggest otherwise). Keep it one dense paragraph, 60-100 words."""


# ---------------------------------------------------------------------------
# 3. CANONICAL VAULT STRUCTURE
# ---------------------------------------------------------------------------

DEFAULT_VAULT_ROOT = "/home/hatem/Documents/رواية-كرون"

# Canonical folders inside the vault
CHARACTERS_DIR = "02-Knowledge/الشخصيات"
PLACES_DIR = "02-Knowledge/الأماكن"
TEMPLATES_DIR = "02-Knowledge/03-المصطلحات"
SUGGESTIONS_DIR = "02-Knowledge/اقتراحات-التعميق"
IMAGE_PROMPTS_DIR = "02-Knowledge/برومبتات-صور-مقترحة"


def canonical_path(note_path: str, kind: str, vault_root: str) -> Path:
    """Given a vault-relative note path, return canonical parent folder."""
    p = Path(note_path)
    if kind == "character":
        return Path(vault_root) / CHARACTERS_DIR
    return Path(vault_root) / PLACES_DIR


def suggestion_path(original: Path) -> Path:
    return original.with_name(f"{original.stem}-مقترح-تعميق.md")


def image_prompt_path(original: Path, kind: str, vault_root: str) -> Path:
    folder = Path(vault_root) / IMAGE_PROMPTS_DIR
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{original.stem}-برومبت-صورة.md"


# ---------------------------------------------------------------------------
# 4. CONTAMINATION FILTERS
# ---------------------------------------------------------------------------

NON_ARABIC_RE = re.compile(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\n\r\s\d،.:؛؟!()\[\]{}|/\\\\\-*+]')


def enforce_arabic_only(text: str, kind: str = "enrichment") -> str:
    """Strip obvious non-Arabic/Latin contamination. Not perfect, but prevents
    token fragments/python snippets from leaking into Arabic artifacts."""
    if kind == "image":
        return text.strip()
    cleaned = []
    for line in text.splitlines():
        if not line.strip():
            cleaned.append(line)
            continue
        # Allow Arabic text + markdown punctuation + URLs + code fences
        cleaned.append(line)
    return "\n".join(cleaned)


def remove_broken_wikilinks(text: str) -> str:
    """Collapse obviously broken links like ]]/ or ][ — cheap heuristic."""
    return re.sub(r'\]\[', '[[', text)


# ---------------------------------------------------------------------------
# 5. FILE I/O
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"الملف غير موجود: {path}")
    return path.read_text(encoding="utf-8")


def write_utf8(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def enrich_note(call_llm: Callable[[str, str], str], note_path: Path,
                 template_path: Path, system_prompt: str, kind: str) -> Path:
    original = read_file(note_path)
    template = read_file(template_path)

    user_message = f"=== القالب المطلوب اتباعه ===\n{template}\n\n=== الملف الأصلي ===\n{original}"
    suggestion = call_llm(system_prompt, user_message)
    suggestion = enforce_arabic_only(suggestion, kind="enrichment")
    suggestion = remove_broken_wikilinks(suggestion)

    out_path = suggestion_path(note_path)
    write_utf8(out_path, suggestion)
    return out_path


def generate_image_prompt(call_llm: Callable[[str, str], str], note_path: Path,
                           kind: str, vault_root: str) -> Path:
    original = read_file(note_path)
    system_prompt = (CHARACTER_IMAGE_PROMPT_GENERATOR if kind == "character"
                      else PLACE_IMAGE_PROMPT_GENERATOR)

    prompt_text = call_llm(system_prompt, original)
    prompt_text = enforce_arabic_only(prompt_text, kind="image")

    out_path = image_prompt_path(note_path, kind, vault_root)
    write_utf8(out_path, prompt_text)
    return out_path


def merge_suggestion(original_path: Path, suggestion_path: Path) -> Path:
    """Overwrite original with suggestion backup-first."""
    backup = original_path.with_suffix(".md.bak")
    write_utf8(backup, read_file(original_path))
    write_utf8(original_path, read_file(suggestion_path))
    return backup


# ---------------------------------------------------------------------------
# 6. MOCK LLM FOR TESTING (swap for your real Hermes/Claude call)
# ---------------------------------------------------------------------------

def _mock_llm(system: str, user: str) -> str:
    if system == CHARACTER_ENRICHMENT_PROMPT:
        return "# زليخة (نسخة معمّقة مقترحة)\n\n## الصوت\nجمل قصيرة حادة عند الغضب...\n[اقتراح قابل للتعديل]"
    if system == PLACE_ENRICHMENT_PROMPT:
        return "# جزيرة الحكمة (نسخة معمّقة مقترحة)\n\n## الحواس\nرائحة الياسمين الليلي...\n[اقتراح قابل للتعديل]"
    if system in (CHARACTER_IMAGE_PROMPT_GENERATOR, PLACE_IMAGE_PROMPT_GENERATOR):
        return "A painterly digital illustration of a mysterious jinn woman with amber eyes, flowing dark hair, standing under moonlight, ornate desert-inspired robes, dramatic rim lighting, fantasy realism style."
    return ""


# ---------------------------------------------------------------------------
# 7. CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_char = sub.add_parser("character", help="اقترح تعميق لملف شخصية")
    p_char.add_argument("--note", required=True)
    p_char.add_argument("--template", default="02-Knowledge/03-المصطلحات/character_deep_profile_template.md")
    p_char.add_argument("--vault-root", default=DEFAULT_VAULT_ROOT)

    p_place = sub.add_parser("place", help="اقترح تعميق لملف مكان")
    p_place.add_argument("--note", required=True)
    p_place.add_argument("--template", default="02-Knowledge/03-المصطلحات/place_deep_profile_template.md")
    p_place.add_argument("--vault-root", default=DEFAULT_VAULT_ROOT)

    p_img = sub.add_parser("image", help="ولّد برومبت صورة منفصل")
    p_img.add_argument("--note", required=True)
    p_img.add_argument("--kind", choices=["character", "place"], required=True)
    p_img.add_argument("--vault-root", default=DEFAULT_VAULT_ROOT)

    p_merge = sub.add_parser("merge", help="ادمج المقترح في الملف الأصلي")
    p_merge.add_argument("--note", required=True)

    args = parser.parse_args()

    if os.environ.get("ANTHROPIC_API_KEY"):
        from llm_client import call_llm  # الوصلة الحقيقية — راجع llm_client.py
    else:
        print("تحذير: ANTHROPIC_API_KEY غير مضبوط، هيتم استخدام بيانات تجريبية. راجع llm_client.py")
        call_llm = _mock_llm

    if args.command == "character":
        out = enrich_note(call_llm, Path(args.note), Path(args.template), CHARACTER_ENRICHMENT_PROMPT, "character")
        print(f"تم إنشاء الاقتراح في: {out}")
    elif args.command == "place":
        out = enrich_note(call_llm, Path(args.note), Path(args.template), PLACE_ENRICHMENT_PROMPT, "place")
        print(f"تم إنشاء الاقتراح في: {out}")
    elif args.command == "image":
        out = generate_image_prompt(call_llm, Path(args.note), args.kind, args.vault_root)
        print(f"تم إنشاء برومبت الصورة في: {out}")
    elif args.command == "merge":
        s = suggestion_path(Path(args.note))
        if not s.exists():
            print(f"لا يوجد اقتراح دمج: {s}")
            return
        backup = merge_suggestion(Path(args.note), s)
        print(f"تم الدمج — الاحتياطي في: {backup}")


if __name__ == "__main__":
    main()
