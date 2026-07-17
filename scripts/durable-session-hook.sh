#!/usr/bin/env bash
# Durable session hook for cron jobs.
# Usage:
#   durable-session-hook.sh <job_id> checkpoint|<message>
#   durable-session-hook.sh <job_id> resume
set -euo pipefail
JOB_ID="${1:-unknown}"
ACTION="${2:-checkpoint}"
STATE_DIR="/home/hatem/.hermes/profiles/hafsa/scripts/state"
mkdir -p "$STATE_DIR"
STATE_FILE="$STATE_DIR/durable-session-${JOB_ID}.jsonl"
NOW="$(date -Iseconds)"
CUR="$(tail -n 1 "$STATE_FILE" 2>/dev/null || echo '{}')"
case "$ACTION" in
  checkpoint)
    mkdir -p "$STATE_DIR"
    if command -v jq >/dev/null 2>&1; then
      CHECKPOINT="$(jq -n --arg now "$NOW" '{checkpoint:$now}')"
      if [ -n "$3" ]; then
        CHECKPOINT="$(jq --arg msg "$3" '. + {message:$msg}' <<<"$CHECKPOINT")"
      fi
      echo "$CHECKPOINT" >> "$STATE_FILE"
    else
      printf '{"checkpoint":"%s","message":"%s"}\n' "$NOW" "${3:-}" >> "$STATE_FILE"
    fi
    ;;
  resume)
    LAST="$(tail -n 1 "$STATE_FILE" 2>/dev/null || echo '{}')"
    if [ "$LAST" = '{}' ]; then
      echo "NO_LAST=1"
      exit 0
    fi
    echo "$LAST"
    ;;
  *)
    echo "Usage: $0 <job_id> checkpoint [note]|resume" >&2
    exit 1
    ;;
esac
