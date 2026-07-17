---
name: arabic-video-summary
description: >
  MUST USE when producing Arabic video summaries for the user. Defines the required
  output skeleton, priority-ranking rules, and output discipline.
  Trigger phrases: لخص الفيديو، كيفاش، ملخص، ارتب بالأولويات، priority summary.
  NOT for: full transcripts, subtitle translation, long-form articles.
---

# Arabic Video Summary

## Required Output Skeleton

Use this exact skeleton unless the user explicitly asks for something different:

```
## 📋 ملخص الفيديو
...overview paragraph only...

## 🔍 الخصائص مرتبة حسب الأولوية
| الأولوية | المفهوم | الوصف |
|---|---|---|
| ⭐⭐⭐ | ... | ... |

## 🎯 مفاهيم رئيسية
| المفهوم | الوصف |
|---|---|
| ... | ... |

## 💡 اللي مفيد ليك أنت/حاتم
| الأولوية | التطبيق | ملاحظات |
|---|---|---|
| ⭐⭐⭐ | ... | ... |

## ⚠️ تحذيرات مهمة
- ...
```

## Output Discipline
- Output the formatted summary immediately.
- Do NOT preface with meta-commentary like "باشتغل على...".
- No filler headers or transitional prose around the structured sections.
- Backup-before-apply: if the user asks to apply changes after the summary, create a backup first: tar.gz the affected vault/project folder under an `Archive/` directory with a timestamped filename, then proceed.

## Application Protocol (MUST USE on apply requests)
After the summary, map the top 1-3 ranked concepts to the user's actual projects/vaults and propose concrete next-step actions tied to known context: health, novel writing, World Cup, daily automation, AI assistants (Lola/Dina), vault structure.
- If the user says "ok", "اعمل", or equivalent terse continuation, immediately begin executing the highest-priority implementation without asking again.
- Execution must produce real artifacts: files, cron jobs, scripts, vault notes, or actual tool calls. Do not stop at describing what could be done.

## Priority Ranking
Apply priority ranking when the user asks to summarize and rank importance.
Rank concepts and applications by relevance to user's context: health, novel writing, World Cup, projects, daily automation.
Use ⭐⭐⭐ for highest priority.
Prefer tables for ranked items over prose / bullet lists.

## Transcript Fetching
Only use `fetch_transcript.py` if it actually exists at `SKILL_DIR/scripts/fetch_transcript.py`. If it is missing, go straight to the `yt-dlp` fallback. Do not block on a missing helper script.

## fetch fallback order
Use this when `fetch_transcript.py` fails because `youtube-transcript-api` is unavailable in this environment.

1. **Check without installing:** `python3 -c "import youtube_transcript_api; print('ok')"`
2. If module is already present on `PYTHONPATH`, run the helper with system python directly: `python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps`
3. If missing, try `uv pip install --system youtube-transcript-api`
4. If that fails due to permissions or missing venv, prefer a user-target install rather than `/usr/local/lib/...`:

```bash
uv pip install --python "$(command -v python3)" --target "$HOME/.local/lib/python3.14/site-packages" youtube-transcript-api
```

5. If still unavailable, switch to `yt-dlp` subtitle fallback instead of blocking.

## youtube-transcript-api install fallback
Only if `fetch_transcript.py` exists but fails due to missing `youtube-transcript-api`, install into the user site-packages directory:

```bash
uv pip install --python "$(command -v python3)" --target "$HOME/.local/lib/python3.14/site-packages" youtube-transcript-api
```

If the helper script still reports the package as missing after that, set the runtime path explicitly:

```bash
PYTHONPATH="$HOME/.local/lib/python3.14/site-packages:$PYTHONPATH" /usr/bin/python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps
```

## Workflow
1. Fetch transcript: prefer `fetch_transcript.py` only if present; otherwise use `yt-dlp` fallback.
2. Validate transcript is non-empty and correct language.
3. If manual subtitles are missing, fetch auto-generated Arabic captions instead.
4. Clean chunked auto-captions before summarizing: auto-captions repeat overlapping sentence fragments, so deduplicate collapsed sequences before transforming into prose.
5. Transform into the Arabic structured summary skeleton, combining both transcript and video description when both are available.
6. Re-read output for coherence before delivering.

## Auto-Caption Cleanup Pattern
YouTube auto-generated subtitles are chunked: each caption segment repeats the tail of the previous one. After downloading as SRT, collapse the repeated tails to produce clean prose.

## Robust fetch order
Use this when `fetch_transcript.py` or `youtube-transcript-api` is unavailable in this environment.

1. **Preferred:** `yt-dlp --skip-download --write-auto-sub --sub-langs ar,en --convert-subs srt "URL"`
2. If subtitle download fails, tell the user transcripts/subtitles are unavailable for that video.
3. Clean the SRT before summarizing with the pattern below.

### Subtitle download throttling
YouTube may return `HTTP Error 429: Too Many Requests`. Do not loop on this.
- Prefer one longer backoff, then one retry.
- If 429 persists after that retry, report the blocker and stop. Do not keep retrying blindly.

### yt-dlp output discovery
`yt-dlp` may write subtitle files next to the current working directory using title-based filenames including the video ID, such as `Build an AI Agent ... [<id>].en.srt`, not only `/tmp/yt_*.srt`. After running `yt-dlp`, locate subtitle files with:

```bash
find /tmp /home/hatem -name '*<video_id>*.srt' 2>/dev/null
```

Use the first existing `.ar.srt` or `.en.srt` file returned.

### Auto-retry on empty transcript
`fetch_transcript.py` can return `{"error":"No transcript found. Try specifying a language with --language."}` even for videos that do have captions. Before falling back to yt-dlp, retry once with explicit likely languages:

```bash
python3 fetch_transcript.py "URL" --language ar,en --timestamps
```

If that still returns empty or errors, proceed to the yt-dlp fallback below.

### Stable SRT → transcript post-processing
```bash
python3 - <<'PY'
from pathlib import Path
import re
path = Path(next(Path('/tmp').glob('yt_*.srt')))
text = path.read_text(encoding='utf-8', errors='ignore')
lines = text.splitlines(keepends=False)
out = [line for line in lines if not re.fullmatch(r'\d+', line.strip())]
text = '\n'.join(out)
blocks = re.split(r'\n\s*\n', text.strip())
segments = []
for block in blocks:
    ls = [line.strip() for line in block.splitlines() if line.strip()]
    if not ls:
        continue
    m = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}', ls[0])
    start = m.group(1) if m else '00:00:00,000'
    content = ' '.join(ls[1:]) if m else ' '.join(ls)
    segments.append((start, content))
merged = []
last = None
start = None
for ts, c in segments:
    if c != last:
        if last:
            merged.append((start, last))
        start = ts
        last = c
if last:
    merged.append((start, last))
final = []
last_text = ''
last_ts = '00:00:00,000'
for ts, c in merged:
    words = c.split()
    prev_words = last_text.split()
    if len(prev_words) > 2 and len(words) > 2 and ' '.join(prev_words[-3:]) in ' '.join(words[-3:]):
        last_ts = ts
        last_text = c
        continue
    final.append((last_ts, last_text))
    last_ts = ts
    last_text = c
if last_text:
    final.append((last_ts, last_text))
out_path = path.with_suffix('.en.md')
markdown = ['# Transcript', ' Time | Text ', '--- | ---']
for ts, c in final:
    if not c:
        continue
    markdown.append(f"`{ts.replace(',', '.')}` | {c}")
out_path.write_text('\n'.join(markdown), encoding='utf-8')
print(f"wrote {len(final)} segments to {out_path}")
PY
```

### yt-dlp subtitle fetch commands
```bash
yt-dlp --skip-download --write-auto-sub --sub-langs ar,en --convert-subs srt 'URL' 2>&1
```

Use `--sub-langs ar,en` instead of separate `--write-auto-sub` calls when both Arabic and English subtitles may exist.

**Pitfall:** `yt-dlp` may emit version-age and challenge-solver warnings even when subtitles download successfully. Treat non-zero subtitle download lines as success signals; ignore the informational warnings.

**Pitfall:** `yt-dlp` may save subtitle files in the current working directory with a title-based filename, not `/tmp/yt_<id>.srt`. After running, discover files by video ID glob in both `/tmp` and the working directory before cleaning.

## Environment / install fallback
If `uv pip install` fails because no venv exists or system `/usr/local/lib/...` is unwritable, check whether system Python already has `youtube_transcript_api` before forcing a retry:

```bash
python3 -c "import youtube_transcript_api; print('ok')"
```

If it prints `ok`, run the helper script directly with `python3`. Only then consider a user-site install:

```bash
uv pip install --python "$(command -v python3)" --target "$HOME/.local/lib/python3.14/site-packages" youtube-transcript-api
PYTHONPATH="$HOME/.local/lib/python3.14/site-packages:$PYTHONPATH" python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps
```

If the package still cannot be imported or the helper still errors, do not loop on `uv`; switch to the `yt-dlp` subtitle fallback immediately.
