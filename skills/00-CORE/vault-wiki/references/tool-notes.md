# Tool & Workflow Notes — 2026-06-22

## Web Tools Status
- **web_search**: NOT working — requires FIRECRAWL_API_KEY or FIRECRAWL_API_URL
- **web_extract**: NOT working — same Firecrawl dependency
- **Workaround**: Use `browser_navigate` + `browser_console` with JS evaluation instead

## Hermes Update
- `hermes update` command: blocked by tool safety (requires user confirmation)
- **Workaround**: `cd ~/.hermes/hermes-agent && git pull && pip install -e . --quiet`
- Current: v0.17.0 (2026.6.19), 77 commits behind upstream

## Obsidian on This System
- Obsidian CLI installed at `/home/hatem/.npm-global/bin/obsidian` (v0.5.1)
- Obsidian desktop app IS installed (plugins exist in vault `.obsidian/` dirs)
- **Plugins CANNOT be installed from CLI** — must use GUI: Settings → Community Plugins
- Plugin folders are empty (no plugins installed yet)

## Logseq Integration
- Logseq v0.10.15 installed via flatpak
- Graph created at `~/.logseq/graphs/hatem-nad/`
- Symlink pattern: `ln -sf /path/to/vault/file.md ~/.logseq/graphs/hatem-nad/pages/Safe-Name.md`
- Config: `~/.logseq/graphs/hatem-nad/logseq/config.edn` (RTL, Arabic, dark mode, whiteboards)
- Sync script: `~/.hermes/profiles/hafsa/scripts/logseq-vault-sync.sh`
- 151 pages synced (Hatem + Hafsa vaults)
- Daily cron at 7AM

## Emoji Path Pitfall
- Hafsa vault folders with emoji in Obsidian display name (e.g. `📰 تقارير/`) may have different actual filesystem paths (e.g. `تقارير/`)
- Always verify with `ls` before hardcoding paths in scripts
