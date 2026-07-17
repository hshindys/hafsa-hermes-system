# Large Transcript Processing — Real-World Pattern

## Session: Hermes Use Cases Video (52K chars)
**Video:** https://www.youtube.com/watch?v=6BHh8BoKim4
**Date:** 2026-06-25

## Challenge
YouTube video transcript was 52,608 characters — too large to process in a single context window.

## Workflow Used

### Step 1: Fetch with timestamps
```bash
cd SKILL_DIR && uv run python3 scripts/fetch_transcript.py "URL" --text-only --timestamps 2>/dev/null > /tmp/transcript.txt
wc -c /tmp/transcript.txt  # Check size
```

### Step 2: Read in chunks
Used `read_file` with offset/limit to read ~300 lines at a time:
- Lines 1-200 (intro + first use cases)
- Lines 201-500 (mid-section: memory, desktop app)
- Lines 501-800 (Slack/Discord, video editing)
- Lines 801-1218 (interview setup, research reports, skill-ification)

### Step 3: Synthesize across chunks
After reading all chunks, synthesized into structured Arabic summary with:
- ملخص عام (one paragraph)
- جدول الاستخدامات (table: person | use case | notes)
- مفاهيم رئيسية (glossary table)
- اقتراحات للتطبيق (priority-ranked: ⭐⭐⭐, ⭐⭐, ⭐)
- تحذيرات مهمة (warnings)

## Key Lessons

1. **Always use `--text-only --timestamps`** — cleaner output, timestamps help with chapter detection
2. **Save to /tmp first** — avoids terminal buffer issues with large output
3. **Read in 200-300 line chunks** — fits context window comfortably
4. **Build synthesis progressively** — after each chunk, note key points; merge at end
5. **For Arabic output** — use the enhanced format from the SKILL.md (tables, priority stars)

## When to chunk
- >30K chars: definitely chunk
- 15-30K chars: chunk if dense technical content
- <15K chars: process normally
