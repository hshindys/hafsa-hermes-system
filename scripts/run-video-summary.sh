#!/usr/bin/env bash
# Video summary cron runner
# Usage: ./run-video-summary.sh <YouTube_URL>
# Output: Markdown summary saved to ~/Documents/Hafsa/AI-News-Sweep/Video-Summaries/

set -euo pipefail

URL="${1:?Usage: $0 <YouTube_URL>"
DATE=$(date +%Y-%m-%d)
OUTDIR="$HOME/Documents/Hafsa/AI-News-Sweep/Video-Summaries"
mkdir -p "$OUTDIR"

VIDEO_ID=$(echo "$URL" | grep -oP 'v=[\w-]{11}' | head -1 | cut -d= -f2)
[[ -z "$VIDEO_ID" ]] && VIDEO_ID=$(echo "$URL" | grep -oP 'youtu\.be/[\w-]{11}' | cut -d/ -f2)
[[ -z "$VIDEO_ID" ]] && { echo "ERROR: Cannot extract video ID"; exit 1; }

SKILL="$HOME/.hermes/profiles/hafsa/skills/06-SYSTEM/media/youtube-content/scripts/fetch_transcript.py"
[[ ! -f "$SKILL" ]] && { echo "ERROR: fetch_transcript.py not found"; exit 1; }

TRANSCRIPT=$(uv run python3 "$SKILL" "$URL" --text-only --language en 2>/dev/null)
[[ -z "$TRANSCRIPT" ]] && { echo "ERROR: Empty transcript"; exit 1; }

# Save transcript
TRANSCRIPT_FILE="$OUTDIR/${DATE}_${VIDEO_ID}_transcript.txt"
echo "$TRANSCRIPT" > "$TRANSCRIPT_FILE"

# Output summary for Hermes agent to process
cat <<EOF
VIDEO_SUMMARY_REQUEST
URL: $URL
VIDEO_ID: $VIDEO_ID
DATE: $DATE
TRANSCRIPT_FILE: $TRANSCRIPT_FILE
CHARS: $(echo "$TRANSCRIPT" | wc -c)
EOF
