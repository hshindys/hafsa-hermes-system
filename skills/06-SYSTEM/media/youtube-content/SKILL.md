---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use
leading words:`transcript`, `youtube-summary`, `chapter-summary`, `threadify`

## Standing rules (apply for the whole session)
1. `transcript`: prefer the helper script over raw web fetch; retry without language filter if empty
2. `youtube-summary`: default format is concise summary unless another format is requested
3. `chapter-summary`: group by topic shifts with timestamps
4. `threadify`: keep each post under platform limits
5. `archive`: save long transcripts/outputs under `/tmp/`

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

Use `uv` so the dependency is installed into the same Hermes-managed environment
that runs the helper script:

```bash
uv pip install youtube-transcript-api
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
uv run python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
uv run python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
uv run python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
uv run python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Priority summary**: Priority-sorted takeaway list for quick action
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps
- **Arabic structured summary**: when user asks in Arabic, produce:
  - ملخص عام
  - خصائص/مفاهيم مرتبة حسب الفئة (جداول)
  - اقتراحات عملية للتطبيق

### Example — Arabic Structured Summary
```
## 📋 ملخص الفيديو
...overview...

## 🔍 الخصائص مرتبة حسب الفئة
| الفئة | المفهوم | الوصف |
|---|---|---|
| ... | ... | ... |

## 💡 اقتراحات للتطبيق
| الأولوية | التطبيق |
|---|---|
| عالية | ... |
```

### Example — Priority Summary
```
1. Setup: one CLI command
2. Model: Moonshot Kimiko 2.6 via OpenRouter
3. Risk: do not expose the API key
```

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps` via `uv run python3`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

## Priority-Ranking Workflow (User Preference)

When user asks to "summarize + rank by priority" or "arrange by importance" for ANY content (YouTube, news, research, documents), use this workflow:

1. Extract key concepts/takeaways from the content
2. Rank by relevance to the user's stated context (health, novel, world cup, etc.)
3. Output as priority-ordered tables with ⭐ ranking (⭐⭐⭐ = highest)
4. Include actionable suggestions mapped to the user's projects
5. Add warnings/caveats if applicable

This is a class-level workflow — not limited to YouTube. Apply when user says:
- "لخص ورتب حسب الأولوية"
- "ن نشوف ونلخص ونرتب"
- "إيه الأهم؟"
- "ارتب بالأولويات بالنسبة لينا"

## Arabic Structured Summary — Enhanced Format (Real Example)

When asked to summarize a video about AI tools, workflows, or use cases in Arabic, extend the basic format to include:

1. **ملخص عام** — one paragraph overview
2. **جدول الاستخدامات/المفاهيم** — columns: الفئة | الاستخدام/المفهوم | ملاحظات
3. **مفاهيم رئيسية** — bulleted glossary of key terms mentioned
4. **اقتراحات للتطبيق** — table with ⭐ priority ranking (⭐⭐⭐ = highest)
5. **تحذيرات مهمة** — any pitfalls or caveats mentioned by speakers

### Real Example Output (AI agent use cases video):
```markdown
## 📋 ملخص الفيديو
حلقة تفاعلية بين أندرو وإريك سو عن استخدامات عملية لـ Hermes agent.
قدم 5 من رواد الأعمال استخداماتهم العملية.

## 🔍 الاستخدامات العملية (مرتبة حسب الأولوية)
| # | الشخص | الاستخدام | ملاحظات |
|---|---|---|---|
| 1 | أندرو | سوم كمبيوتر - Copy Google Loop | يشتغل بالليل بدون تدخل |
| 2 | أليكس | بحث عن المنافسين | markdown → Claude Code |
...

## 🎯 مفاهيم رئيسية
| المفهوم | الوصف |
|---|---|
| Loop | تكرار مهمة لحد ما تخلص |
| Cron Job | مهمة مجدولة تلقائياً |
...

## 💡 اقتراحات للتطبيق
| الأولوية | التطبيق |
|---|---|
| ⭐⭐⭐ | Loop |
| ⭐⭐⭐ | Resolver |
...

## ⚠️ تحذيرات مهمة
- Kanban Board لسه مش mature
- متحملش SSDs كتير
```

## Summary

See `references/large-transcript-processing.md` for the real-world pattern for 50K+ char transcripts.
See `references/arabic-summary-real-example.md` for a full real-world example of the enhanced Arabic structured summary format (priority-ranked use cases, concept glossary, actionable suggestions, warnings).
See `references/data-verification-from-authoritative-sources.md` for the verification protocol before writing structured data (World Cup 2026 lesson).

## Large Transcripts (>30K chars)

When a video produces a very long transcript (50K+ chars), do NOT try to process it in one pass. See `references/large-transcript-processing.md` for the proven chunk-and-synthesize workflow.

Quick version:
1. Save to `/tmp/transcript.txt` via `> /tmp/transcript.txt`
2. Read in 200-300 line chunks with `read_file(offset, limit)`
3. Synthesize progressively — note key points per chunk, merge at end

## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: run `uv pip install youtube-transcript-api` and retry.
