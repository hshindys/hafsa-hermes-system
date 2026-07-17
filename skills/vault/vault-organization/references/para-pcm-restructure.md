# PARA/PCM Refactor Notes — Hafsa Vault 2026-07-11

## Applied to
Vault: `/home/hatem/Documents/Hafsa`

## Before → After mapping
- `🚀 Projects/Hermes/` → `01-Projects/Hermes/`
- `🚀 Projects/*.md` + `lead-scraper` + `watermark-tool` + `website-cloner` → `01-Projects/`
- `02-Projects/` → `01-Projects/`
- `02-Work-System/` → `02-Areas/Work-System/`
- `📚 Knowledge/` → `03-Resources/`
- `📚 World of Kron/` → `03-World-of-Kron/` (deduped; old empty tree removed)
- `Journal/2026-07-05.md` → `📅 اليوميات/` (duplicate removed)
- `Knowledge/` remnant → `03-Resources/Misc/`

## Final tree
- `/01-Projects/`
- `/02-Areas/Work-System/`
- `/03-Resources/`
- `/03-World-of-Kron/`
- `/Archive/Old-Al-Ahly-Project/`
- `/Religion/`
- `/📊 Reports/`
- `/📅 اليوميات/`
- `/تقارير/`
- `/scripts/`
- `/tmp/`

## Pitfalls hit
- `mcp_filesystem_move_file` failed with parent-missing and server-unreachable; bash/python moved everything.
- `Journal/` deletion failed because file existed at destination; handled duplicate by removing source.
- `Knowledge/` remnant empty-dir removal required two-pass iteration.

## Arabic skill key phrase
"طبّق المنهجية على الخزنة" → reorganize Hafsa vault into PARA/PCM structure.
