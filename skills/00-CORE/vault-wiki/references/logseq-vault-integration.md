# Logseq + Obsidian Integration

## Setup
- Logseq v0.10.15 via flatpak (`com.logseq.Logseq`)
- Graph: `~/.logseq/graphs/hatem-nad/`
- Config: `~/.logseq/graphs/hatem-nad/logseq/config.edn`

## Symlink Pattern
```bash
# Vault file → Logseq pages
ln -sf "/path/to/vault/file.md" ~/.logseq/graphs/hatem-nad/pages/Safe-Name.md

# Hafsa vault prefix
ln -sf "/path/to/hafsa/file.md" ~/.logseq/graphs/hatem-nad/pages/hafsa--Safe-Name.md
```

## Sync Script
`~/.hermes/profiles/hafsa/scripts/logseq-vault-sync.sh` — syncs both Hatem + Hafsa vaults

## Config Highlights
- RTL enabled (`:ui/rtl? true`)
- Arabic preferred language (`:ui/preferred-language "ar"`)
- Dark theme
- Whiteboards, PDFs, block embeddings enabled
- Journals: daily format `yyyy-MM-dd`

## Current Stats
- 151 pages synced (Hatem + Hafsa vaults)
- 6 journal entries
- Daily cron at 7AM

## How to Open
```bash
flatpak run com.logseq.Logseq
```
Or from desktop application menu.
