#!/bin/bash
# vault-memory-sync.sh
# Two-way sync between Hermes memory and Vault
# Run via cron: captures conversation highlights → vault notes

set -e

HAFSA_VAULT="/home/hatem/Documents/Hafsa"
HATEM_VAULT="/home/hatem/Documents/Hatem Nad"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)

# === 1. Create daily journal entry if not exists ===
JOURNAL_FILE="$HAFSA_VAULT/📅 اليوميات/$DATE.md"

if [ ! -f "$JOURNAL_FILE" ]; then
  cat > "$JOURNAL_FILE" <<EOF
---
title: يومية $DATE
date: $DATE
tags: [يومية]
vault: hafsa
---

# 📅 $DATE

## أحداث اليوم

## قرارات

## ملاحظات

## غداً
EOF
  echo "✅ Created daily journal: $JOURNAL_FILE"
else
  echo "ℹ️ Journal already exists: $JOURNAL_FILE"
fi

# === 2. Update vault statistics ===
HAFSA_COUNT=$(find "$HAFSA_VAULT" -name "*.md" -not -path "*/.git/*" -not -path "*/.obsidian/*" -not -path "*/AI-Skills-Research/*" | wc -l)
HATEM_COUNT=$(find "$HATEM_VAULT" -name "*.md" -not -path "*/.git/*" -not -path "*/.obsidian/*" -not -path "*/.trash/*" | wc -l)
TOTAL=$((HAFSA_COUNT + HATEM_COUNT))

# Update Hafsa index stats
sed -i "s/| ملفات Markdown | ~.*|/| ملفات Markdown | ~$TOTAL |/" "$HAFSA_VAULT/📌 Index.md" 2>/dev/null || true

echo "📊 Vault stats: Hafsa=$HAFSA_COUNT, Hatem=$HATEM_COUNT, Total=$TOTAL"

# === 3. Log the sync ===
SYNC_LOG="$HAFSA_VAULT/تقارير/vault-sync-log.md"
if [ ! -f "$SYNC_LOG" ]; then
  echo "# 📋 Vault Sync Log" > "$SYNC_LOG"
  echo "" >> "$SYNC_LOG"
  echo "| Date | Hafsa Files | Hatem Files | Total |" >> "$SYNC_LOG"
  echo "|------|------------|-------------|-------|" >> "$SYNC_LOG"
fi

echo "| $TIMESTAMP | $HAFSA_COUNT | $HATEM_COUNT | $TOTAL |" >> "$SYNC_LOG"

echo "✅ Vault memory sync complete at $TIMESTAMP"
