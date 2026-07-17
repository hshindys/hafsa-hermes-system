# Video Summary Session Notes — durable lessons

## Backup-before-apply
If the user follows a summary with apply/create/change requests on the vault or projects, create a backup first:
`tar -czf <project>/Archive/backup-YYYYMMDD-HHMMSS.tar.gz -C <project> .`
Do not proceed until the backup exists.

## Transcript fallback ordering
Preferred order:
1. `python3 -c "import youtube_transcript_api; print('ok')"`
2. If present, run helper directly with system python:
   `python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps`
3. If missing, `uv pip install --python "$(command -v python3)" --target "$HOME/.local/lib/python3.14/site-packages" youtube-transcript-api`
4. If still unavailable, retry with explicit `PYTHONPATH=...` wrapper
5. If still failing, switch to `yt-dlp` subtitle fallback

Do not loop on installs; switch to `yt-dlp` instead.

## User expectations
- Priority tables over prose.
- Immediate backup when asked to apply.
- No meta-commentary before the structured summary.
- Use ⭐⭐⭐ for top items.
- After summary, if user confirms tersely ("ok"/"اعمل"/"do it"), immediately execute highest-priority implementation artifacts instead of stopping at recommendations.

## yt-dlp subtitle behavior observed
- `HTTP Error 429: Too Many Requests` on `ar`: sleep 20s, then retry `--sub-langs en` only.
- Subtitles often save with title-based filename in current working directory, not `/tmp`.
- Ignore version/jsc/impersonation warnings when subtitle `.srt` was produced successfully.

## Auto-caption cleanup cue
- Arabic auto-captions often deduplicate to many empty segments. If output is mostly empty, prefer English auto-captions if they exist; they usually retain more technical content density.

## Application protocol
- After summary, produce concrete next-step actions tied to known user context.
- If user confirms tersely, immediately begin executing top-priority implementation.
- Execution must create real artifacts: files, scripts, cron jobs, vault notes, tool calls.
