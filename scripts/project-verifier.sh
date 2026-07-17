#!/usr/bin/env bash
# Verifier: read last line of durable session state and enforce pass/fail.
# Usage: project-verifier.sh <job_id> [require_checkpoint=1]
set -euo pipefail
JOB_ID="${1:-unknown}"
REQUIRE="${2:-1}"
STATE_DIR="/home/hatem/.hermes/profiles/hafsa/scripts/state"
STATE_FILE="$STATE_DIR/durable-session-${JOB_ID}.jsonl"
if [ ! -f "$STATE_FILE" ]; then
  echo "VERIFIER=FAIL no_state_file"
  exit 1
fi
LINES="$(wc -l < "$STATE_FILE")"
if [ "$REQUIRE" = "1" ] && [ "$LINES" -lt 1 ]; then
  echo "VERIFIER=FAIL no_checkpoint"
  exit 1
fi
LAST="$(tail -n 1 "$STATE_FILE")"
if [ "$LAST" = '{}' ] || [ -z "$LAST" ]; then
  echo "VERIFIER=FAIL empty_checkpoint"
  exit 1
fi
RETRIES="$(grep -c '"checkpoint"' "$STATE_FILE" 2>/dev/null || echo 0)"
echo "VERIFIER=PASS checkpoints=$RETRIES last=$LAST"
exit 0
