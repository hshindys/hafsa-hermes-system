# Round-of-16 creation pattern for large tournaments

Use this when converting completed Round-of-32/group-stage results into Round-of-16 match listings.

## Sequence

1. Update `📚 Knowledge/World Cup 2026/Knockout Stage.md`:
   - Replace generic TBD slot in the Round-of-32 table with the new confirmed teams/result.
   - Then update the Round-of-16 table rows directly with the actual matchup or `Team A / Team B` if still pending.
2. Create individual match-page files under `📚 Knowledge/World Cup 2026/` for each R16 fixture, including:
   - frontmatter tags: `world-cup`, `knockout`, and any relevant region tag
   - match/teams/date/stadium/status
   - notes on how each side qualified, especially winners/runners-up/best third qualifiers
3. For pending opponents whose R32 match is still ongoing:
   - label as `Team A / Team B`
   - add a note: result pending Match NN
4. Do not create match files before the main bracket table reflects the new matchups.

## Vault paths

- Knockout stage table: `📚 Knowledge/World Cup 2026/Knockout Stage.md`
- Match pages: `📚 Knowledge/World Cup 2026/<Team1> vs <Team2> - Round of 16.md`

## Notes

- Always include Cairo/UTC+3 dates in match files, but keep dates in the bracket table concise.
- When a user provides a score inline, update the main knockout file first, then reassess pending R16 slots immediately.
- Same-group teams cannot meet in the R16 unless bracket structure forces it; flag and do not write.
