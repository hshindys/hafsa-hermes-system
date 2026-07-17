# Cron Maintenance Notes — 2026-06-27

Source: nightly second-brain cron run on Hafsa vault.

## Observed patterns
- sibling cron writer already wrote `/home/hatem/Documents/Hafsa/.hermes-cron/second-brain-report/06-27-2026.md` before this agent read it.
- fix: read-then-patch, not blind write.
- repeated `mcp_vault_*_list_notes` as change detection is slow; prefer `mcp_vault_*_recent_notes` + `mcp_vault_*_find_orphans` for nightly sweeps.
- daily note creation is cheap and preferred when the template is available.

## Tooling TODO currently pending
- Piper TTS Arabic ONNX model invalid locally (`ar_JO-suad-medium`, `ar_JO-sultana-medium` broken); not a feature failure, model-fetch issue.
- PenPot: `docker-compose.yaml` fetch was 404; direct install docs URL required next.
- World Monitor: missing package name on pip; locate it via GitHub or package registry first.