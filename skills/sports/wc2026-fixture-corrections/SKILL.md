---
name: wc2026-fixture-corrections
description: Use when the user corrects knockout-stage dates or matchups for World Cup 2026, or when fixture slots need to be rerouted after eliminating teams. Must USE for phrases such as "مباريات ايامها متبدلة", "المغرب قابلت فرنسا", "انجلترا الارجنتين 15", or any "no, actually X on Y" correction.
---

# WC 2026 Fixture Corrections

## Trigger
- User says a knockout date/matchup is wrong.
- User provides replacement slate, e.g., "X vs Y on DATE".
- Eliminated-team slots need rerouting after an incorrect placeholder.

## Inputs
- Vault roots: Hafsa (`📚 Knowledge/World Cup 2026/`) and Hatem (`01-Projects/World Cup 2026.md`).
- Canonical knockout file: `📚 Knowledge/World Cup 2026/Knockout Stage.md`.

## Workflow
1. Acknowledge user-confirmed slate without further external verification; they are authoritative.
2. Read affected knockout sections in both knockout file and Hatem tracker.
3. Patch semifinal/final/quarter rows to match user-confirmed dates and opponents.
4. Remove stale "winner of A vs B" placeholders once a concrete matchup is supplied.
5. Refresh session timestamp to current Cairo date and note the correction source as "user-confirmed fixture correction".
6. Re-scan the knockout table for duplicate opponents/dates; if found, ask the user before rerouting.

## Output contract
- Deliver a concise confirmation with only the corrected rows, then update vault files.

## Key rules
- User's fixture corrections override template bracket order and any cached Wikipedia/Goal ordering.
- Cairo time is the default for all fixtures.
- Do not invent venues or sources when unknown; leave empty if not confirmed.
- Do not block on external verification when user explicitly states new dates/matchups.

## Anti-patterns
- Do not continue showing old fixture order after correction.
- Do not add seafood mentions in match notes.
- Do not silently leave "winner of X vs Y" text when actual opponents are known.
- Do not mix match-page paths across group-stage and knockout-stage folders.
- **External-source failure is not a blocker:** when live verification fails—X credits exhausted, Wikipedia/Google blocked—treat user-supplied results as authoritative and patch directly.
- **Stale-placeholder rerouting:** if a corrected matchup leaves a previous slot obsolete, reconcile it immediately instead of asking the user to re-explain.
- **Avoid double-narrating verified state:** after the user corrects you, patch and report the corrected table only; do not repeat the prior wrong state as justification.
