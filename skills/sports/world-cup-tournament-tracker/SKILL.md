---
name: world-cup-tournament-tracker
description: >
  Track a FIFA World Cup/knockout tournament end-to-end inside the user's vault.
  MUST USE when updating brackets, recording match results, writing match-page notes,
  handling eliminations/advancements, or resolving user corrections to fixtures,
  dates/times, or matchups. Trigger phrases: "World Cup", "كأس العالم", "Round of 16",
  "دور الـ 16", "مباراة", "knockout", "نتيجة مباراة", "تصفيات", "تأهلت", "خرجت".

inputs:
  - Vault world-cup notes under `📚 Knowledge/World Cup <year>`
  - User-supplied results and fixture corrections in Arabic RTL
  - Cairo-time zone rules for all times

outputs:
  - Updated knockout-stage bracket in `Knockout Stage.md`
  - Per-match pages as `Team A vs Team B - Round of N.md`

preferences:
  - All vault content in Arabic RTL only
  - Times in Cairo (UTC+3) by default
  - No seafood references in tournament notes
---

# World Cup Tournament Tracker

Maintain a trusted vault-backed knockout tracker for World Cup tournaments, with
user-supplied results, per-match pages, and conflict resolution.

## Core workflow

1. Read existing state first from:
   - `Knockout Stage.md`
   - Any match-page files under the tournament folder.

2. Apply each user correction in exact order: result, bracket alignment,
   elimination, advancement, new match.

3. Edit `Knockout Stage.md` directly using patch/read cycle when exact string
   matching fails; do not guess-match against outdated table state.

## Bracket rules

- Do not invent unconfirmed fixtures from external sources; only advance a team
  when user confirms it as qualified.
- When team is eliminated, remove or update its slot rather than leaving invalid
  matchups.
- Simultaneous slot conflicts are invalid: same team appears in only one active
  match at the same stage.

## Match pages

Write one note per confirmed match with:
`⸻⸻⸻ tags: ["world-cup"]` etc.

Include: Stage, Date, Time in Cairo, Status, Stadium, Notes.
Keep Status short: `Pending`, `User-confirmed matchup`, `Confirmed`, `Completed`.

## Eliminations / auto-advancements

- If team from match A is eliminated and match B references it, replace it
  with `TBD` or available substitute.
- Do not create phantom advanced slots unless user explicitly confirms.

## User corrections and style

- Update bracket in `Knockout Stage.md` first, then match pages.
- When user says "X will play Y", create/update that matchup in the bracket immediately and reconcile ALL occurrences, including both the confirmed-results table and any round-of-16 table that still holds obsolete matchups.
- Preserve metadata: source, last-update timestamp, and no-seafood reminder.
- **Stage-normalization pattern:** when the user reports a result but the file’s headings or placeholders are inconsistent, first align the stage headings/sections, then patch the confirmed result into the correct stage’s matchup line before retrying the same game. Do not duplicate the same match across Round of 32 and Round of 16.
- **Batch entry pattern:** if the user supplies multiple match results in one turn, patch them in exact order before asking anything else. Do not explain or summarize between patches unless the user explicitly asks.

## Time-handling

- Store kickoff times as `HH:MM Cairo (UTC+3)`.
- Sort bracket first by date order, then by user-supplied match order.

## Source handling for delayed/slow live pages
- Goal/365scores often return simplified scores but may fail structure extraction; use Wikipedia as the primary structural source for confirmable fixtures/combinations when those pages do not yield clean match data.
- Do not block an update just because Goal/365scores could not be rendered; a single degraded live source does not imply tournament data is unavailable.
- When journaling an update with sparse external confirmation, still keep Egypt local defaults unless an authoritative source says otherwise.

## Sources and verification order

Use this priority for external result updates:
1. `goal.com`
2. `365scores.com`
3. `en.wikipedia.org/wiki/2026_FIFA_World_Cup` and knockout-stage page

- Cross-check match results across sources; when timestamps conflict, trust the fresher source.
- If a source fails transiently, do not retry it blindly. Fall back to the next source in priority. Do not mark data unavailable because one fetch failed.
- Never treat a single failed fetch as proof a source is broken; capture the retry/fallback pattern, not the original error.
- Do not re-render or quote upstream HTML form in outputs. Extract only the structured result needed for the local tracker.
- If all external sources are unavailable, seed tracker placeholders and rely on manual user-supplied results as ground truth.

## Conflict resolution

- When sources conflict on a score/result, prefer the source with the newest publish/retrieval timestamp.
- Preserve the local file’s table format. Do not rewrite non-table narrative unless the user explicitly asks.
- When user-supplied Egypt data exists locally, keep it unless an authoritative external source explicitly states otherwise.

## Egypt-local defaults

- Keep Egypt MOTM, notes, and local annotations as user-supplied by default.
- Update Egypt advancement/qualification state only when confirmed by an authoritative source.
- When Egypt is eliminated, mark that path clearly in the tracker and reconcile any downstream matchups that referenced the eliminated team.

## Table-only update discipline

- When the task asks for a table-only file update, edit only table rows and stage headings.
- Do not alter unrelated narrative blocks unless the user requests a full-document revision.
- If preserving the exact table formatting is important, read the file fully before patching to match spacing and alignment.

## Unattended/cron update discipline

- Even with no user present, produce a findings-only report; do not narrate reasoning.
- Avoid speculative status commentary—use a minimal reported facts block.
- For Egypt-related rows or notes, keep previously local user-supplied values unless an authoritative external source explicitly states a new value; do not infer or guess Egypt names/scores from tournament context.

## Pitfalls
## Pitfalls
- Vault MCP can return `Note not found` for emoji-prefixed paths; fallback to absolute `/home/hatem/Documents/Hafsa/...` for direct file reads/writes.
- Round-of-16 matchups are variable until bracket is confirmed. Use `TBD` placeholders rather than guessing.
- If patch fails because the file uses different spacing/formatting than expected, re-read the exact file contents before retrying instead of repeating the same patch.
- **Don’t assume user strings map to the same stage:** when the user says "هذه مباريات دور ال 32" or "دوول كانو مباريات دور ال 32 اما مباريات الامس كانت دور ال 16", treat that as a stage correction and normalize headings first, then update results in the right section only.
- **Degraded-source authorization rule:** when live sources are simultaneously degraded—X blocked by credits, Goal/365scores/Wikipedia blocked or truncated—treat the user’s supplied results as authoritative and patch immediately; do no keep seeking external confirmation. Report only the corrected rows, not the failed verification chain.

## Source notes
- See `references/live-source-behavior-2026.md` for observed live-source behavior and fallback guidance.
- Use Wikipedia as the structural fallback when `goal.com`/`365scores.com` are slow or non-extractable.
- GOAL result/player-rating articles for confirmed knockout matches consistently carry Cairo-timezone timestamps like `Jul 12, 2026 10:00+03:00`; when present, they are authoritative for match outcome and date, but do not invent scores from previews.
