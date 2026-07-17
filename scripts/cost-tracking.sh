#!/bin/bash
# Cost Tracking Script for Hermes Agent
# Logs daily API usage and costs across all platforms

DATE=$(date +%Y-%m-%d)
LOG_DIR="$HOME/.hermes/profiles/hafsa/cron/output"
LOG_FILE="$LOG_DIR/cost-tracking-$DATE.log"

mkdir -p "$LOG_DIR"

echo "=== Cost Tracking — $DATE ===" > "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Check OpenRouter usage (if API key exists)
if [ -n "$OPENROUTER_API_KEY" ] || grep -q "OPENROUTER_API_KEY" "$HOME/.hermes/profiles/hafsa/.env" 2>/dev/null; then
    echo "📊 OpenRouting:" >> "$LOG_FILE"
    OPENROUTER_KEY=$(grep "OPENROUTER_API_KEY" "$HOME/.hermes/profiles/hafsa/.env" 2>/dev/null | cut -d'=' -f2)
    if [ -n "$OPENROUTER_KEY" ]; then
        curl -s "https://openrouter.ai/api/v1/auth/key" \
            -H "Authorization: Bearer $OPENROUTER_KEY" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    d = data.get('data', {})
    print(f'  Credits remaining: {d.get(\"credit_limit\", \"N/A\")}')
    print(f'  Usage today: {d.get(\"usage\", \"N/A\")}')
except:
    print('  Unable to fetch usage')
" >> "$LOG_FILE" 2>/dev/null
    fi
    echo "" >> "$LOG_FILE"
fi

# Check disk usage
echo "💾 Disk Usage:" >> "$LOG_FILE"
du -sh "$HOME/.hermes/profiles/hafsa/" 2>/dev/null | awk '{print "  Hafsa profile: "$1}' >> "$LOG_FILE"
du -sh "$HOME/.hermes/profiles/hafsa/sessions/" 2>/dev/null | awk '{print "  Sessions: "$1}' >> "$LOG_FILE"
du -sh "$HOME/.hermes/profiles/hafsa/skills/" 2>/dev/null | awk '{print "  Skills: "$1}' >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Count active cron jobs
echo "⏰ Active Cron Jobs:" >> "$LOG_FILE"
CRON_COUNT=$(hermes -p hafsa cron list 2>/dev/null | grep -c "job_id\|scheduled" || echo "0")
echo "  Total: $CRON_COUNT" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Session stats
echo "💬 Session Stats:" >> "$LOG_FILE"
SESSION_COUNT=$(find "$HOME/.hermes/profiles/hafsa/sessions/" -name "*.jsonl" 2>/dev/null | wc -l)
echo "  Total sessions: $SESSION_COUNT" >> "$LOG_FILE"
TODAY_SESSIONS=$(find "$HOME/.hermes/profiles/hafsa/sessions/" -name "*$(date +%Y%m%d)*" 2>/dev/null | wc -l)
echo "  Sessions today: $TODAY_SESSIONS" >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "=== End — $DATE ===" >> "$LOG_FILE"

# Keep only last 30 days of logs
find "$LOG_DIR" -name "cost-tracking-*.log" -mtime +30 -delete 2>/dev/null
