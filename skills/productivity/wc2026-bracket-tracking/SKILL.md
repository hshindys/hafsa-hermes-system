---
name: wc2026-bracket-tracking
description: Use when tracking knockout updates for World Cup 2026 in the Hatem/Hafsa vaults, creating or patching match pages and the Knockout Stage.md table, and verifying no duplicate opponents/dates.
---

# WC 2026 Bracket Tracking

## Trigger
- User supplies a knockout result, Round of 16/8/4 matchup, or asks to update the World Cup 2026 bracket.
- Use before guessing opponents; user-confirmed matchups override template bracket order.
- Do NOT use for group-stage tables; only knockout stage files.
- Also triggers for unattended daily World Cup match-results updates where the deliverable is an in-place table refresh, not match-page creation.

## Inputs
- Vault roots: Hafsa (`📚 Knowledge/World Cup 2026/`) and Hatem (`01-Projects/World Cup 2026.md`).
- Canonical knockout file: `📚 Knowledge/World Cup 2026/Knockout Stage.md`.
- Match page template: `references/round-of-16-match-template.md`.

## Workflow
1. Read `Knockout Stage.md` to see pending matches and notes.
2. Patch the knockout table with the user-supplied result or confirmed matchup.
3. Create or update the match-page note for that game, using `references/round-of-16-match-template.md` when applicable.
4. Remove stale placeholder match pages when teams are eliminated or slot is replaced.
5. Re-scan the knockout table for duplicate opponents on the same date; if found, ask the user before rerouting slots (`clarify`).
6. Update the file index/frontmatter if the vault has an index referencing match pages.

## Output contract
- Always: patched `Knockout Stage.md` and updated/created match-page file.
- If no opener was requested: present the current R16/R8 table with status (confirmed/pending/TBD).
- Unattended/no-update runs: do not alter vault files when there is no confirmed new result; emit a minimal status block instead of a silent pass.

## Key rules
- Cairo time is the default; insert `HH:MM Cairo (UTC+3)` whenever the user provides a local time.
- Do not invent venues or sources when unknown; leave stadium empty if not confirmed.
- If a user-confirmed matchup conflicts with existing table slots, surface the conflict explicitly and ask how to reroute — do not silently overwrite other confirmed matchups.
- Eliminated-team cleanup: delete or move the obsolete match-page note for that slot.

## Source handling
- Preferred live sources: Goal.com Arabic first, Wikipedia knockout pages second.
- `365scores.com` often fails simplification from HTML; do not treat a fetch failure there as blocking.
- For unattended/cron updates, if Goal/365scores do not yield clean fixture data, use Wikipedia knockout combinations/the round pages as the authoritative structural source for confirmed matchups and slot mapping.
- Always timestamp against Cairo time and note freshness when sources conflict.
- Do not block on a single failed live source; retry with the priority stack before reporting unable to update.
- If multiple live sources fail in the same session—X credits exhausted, Wikipedia robots-blocked, Goal/365scores unreachable—switch directly to user-supplied results and update the tracker without narration.
## Anti-patterns
- Do not guess third-place qualifier order; wait for user confirmation.
- Do not add seafood mentions in match notes; keep football-only text.
- Do not mix match-page paths across group-stage and knockout-stage folders.
- Do not block on a single failed live source; retry with the priority stack before reporting unable to update.
- After a simultaneous multi-source failure, do not output failure explanations; patch from user confirmation and report only the corrected table rows.
