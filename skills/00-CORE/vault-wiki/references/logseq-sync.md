# Logseq Vault Sync

## Setup (2026-06-22)
- Logseq v0.10.15 installed via flatpak (`com.logseq.Logseq`)
- Graph: `~/.logseq/graphs/hatem-nad/`
- Config: `~/.logseq/graphs/hatem-nad/logseq/config.edn`
- Sync script: `~/.hermes/profiles/hafsa/scripts/logseq-vault-sync.sh`
- Cron: daily 7AM — syncs both Hatem + Hafsa vaults via symlinks

## How it works
- Symlinks markdown files from both vaults into Logseq's `pages/` directory
- Any edit in either vault or Logseq is reflected everywhere (same files)
- Logseq adds: graph view, block references, PDF annotation, whiteboards

## Opening Logseq
```bash
flatpak run com.logseq.Logseq
```
Or from desktop application menu.

## Graph location
Logseq stores graphs in `~/.logseq/graphs/<graph-name>/` with `pages/` and `journals/` subdirectories.