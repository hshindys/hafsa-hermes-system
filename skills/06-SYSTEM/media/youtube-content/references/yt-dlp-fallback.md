# YouTube Summarization — yt-dlp Fallback

When the youtube-transcript-api fails or returns empty, use `yt-dlp` to download auto-generated subtitles:

```bash
# Download English subtitles as SRT
yt-dlp --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
  "https://www.youtube.com/watch?v=VIDEO_ID" -o "/tmp/video_subs"

# Download Arabic subtitles
yt-dlp --write-auto-sub --sub-lang ar --skip-download "URL" -o "/tmp/video_subs"
```

**Note:** YouTube rate-limits subtitle downloads. If you get `HTTP Error 429: Too Many Requests`, wait or try a different language.

**Parsing SRT:** Strip timestamps and deduplicate lines:

```bash
cat video_subs.en.srt | sed '/^$/d' | sed '/^[0-9]/d' | sed 's/<[^>]*>//g' | sort -u | tr '\n' ' '
```

**For long videos:** Transcripts may be incomplete (YouTube caps at ~40KB). In that case, summarize what's available and note the limitation.
