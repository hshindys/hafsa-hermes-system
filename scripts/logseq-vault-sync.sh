#!/bin/bash
# logseq-vault-sync.sh
# Sync Hatem Nad + Hafsa vaults → Logseq graph
# Run daily via cron at 7AM

set -e

HATEM_VAULT="/home/hatem/Documents/Hatem Nad"
HAFSA_VAULT="/home/hatem/Documents/Hafsa"
LOGSEQ_GRAPH="$HOME/.logseq/graphs/hatem-nad"
PAGES_DIR="$LOGSEQ_GRAPH/pages"
JOURNALS_DIR="$LOGSEQ_GRAPH/journals"

mkdir -p "$PAGES_DIR" "$JOURNALS_DIR"

echo "🔄 Syncing vaults → Logseq..."

# Function to sync a vault
sync_vault() {
  local vault_path="$1"
  local prefix="$2"
  local count=0
  
  find "$vault_path" -name "*.md" -type f \
    ! -name ".*" \
    ! -path "*/.obsidian/*" \
    ! -path "*/.trash/*" \
    ! -path "*/.git/*" \
    ! -path "*/AI-Skills-Research/*" \
    ! -path "*/Templates/*" \
    ! -path "*/🔧 Skills/*" \
    ! -path "*/.hermes/*" \
    2>/dev/null | while IFS= read -r file; do
      rel_path="${file#$vault_path/}"
      safe_name="${prefix}$(echo "$rel_path" | sed 's|/|--|g')"
      target="$PAGES_DIR/$safe_name"
      
      if [ -L "$target" ]; then
        current_src=$(readlink "$target" 2>/dev/null || echo "")
        if [ "$current_src" != "$file" ]; then
          ln -sf "$file" "$target"
        fi
      else
        ln -sf "$file" "$target"
      fi
    done
}

# Sync both vaults
sync_vault "$HATEM_VAULT" ""
sync_vault "$HAFSA_VAULT" "hafsa--"

# Sync journals (daily notes)
find "$HATEM_VAULT/02-مفكرة" -name "*.md" -type f 2>/dev/null | while read f; do
  name=$(basename "$f")
  ln -sf "$f" "$JOURNALS_DIR/$name"
done

find "$HAFSA_VAULT/📅 اليوميات" -name "*.md" -type f 2>/dev/null | while read f; do
  name="hafsa-$(basename "$f")"
  ln -sf "$f" "$JOURNALS_DIR/$name"
done

# Count
total_pages=$(find "$PAGES_DIR" -type l 2>/dev/null | wc -l)
total_journals=$(find "$JOURNALS_DIR" -type l 2>/dev/null | wc -l)

echo "✅ Logseq sync: $total_pages pages + $total_journals journals"
