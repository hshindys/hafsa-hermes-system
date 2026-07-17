---
name: sports-scores
description: >
  Fetch sports match results and save them to the user's vault.
  MUST USE when the user asks for match scores, game results, tournament standings,
  football/soccer results, or wants results "put in the vault / saved / updated".
  Covers: fetching live/recent results from the web, formatting as markdown tables,
  and writing/updating a structured results file in the user's second-brain vault.
  Trigger phrases: "جيب نتائج", "نتائج مباريات", "match results", "scores today",
  "حدّث النتائج", "احط النتائج في الخزنة", "كأس العالم", "world cup scores".
---

# Sports Scores to Vault

Fetch football/soccer match results and persist them in the user's vault as structured markdown.

## Workflow

### 1. Determine scope

- Which tournament (World Cup, Champions League, league matches, etc.)
- Which dates (today, yesterday, specific date range, "matchday N")
- Which format (results only, standings, or both)

### 1a. Verify today first

Before presenting or patching any “today” schedule, confirm the current weekday from the system so you don’t display yesterday/tomorrow fixtures under the wrong date. If the live schedule and the file disagree on the date, trust a verified authoritative source (default: Wikipedia knockout bracket/group tables), not the existing vault file.

### 2. Patching existing vault files

When updating an existing results file:

- Prefer `patch` over full rewrites.
- If `patch` returns "Found N matches", widen `old_string` to include at least one unique surrounding line (date header, preceding match row).
- If the same correction applies to every duplicate match (e.g., fixing a typo in every "Spain vs Cape Verde" line), set `replace_all=true`.
- When in doubt, `read_file` the exact region and quote the surrounding lines.

### 3. Write new values

- For new rows: append to the results table using the existing markdown structure.
- For stats/totals: update goals aggregate and average math explicitly.
- For group standings: update played/W/D/L/GF/GA/GD/Pts for every affected team, not just the winner.

but **the user may designate** a specific site as the authoritative source. When the user explicitly sets a score source (e.g. goal.om), that source is treated as required first-choice for updates and override of other data.

**Step-by-step:**

1. Navigate to the tournament's Wikipedia page, e.g. `https://en.wikipedia.org/wiki/2026_FIFA_World_Cup`
2. Wait for page to fully load (these are large pages, 5000+ elements)
3. Use `browser_console` with a JS regex expression to extract match results from the page text. Wikipedia tournament pages use a consistent format wikitable cells.

**JS extraction pattern** (adapt regex to tournament page format):

```
(() => {
  const allText = document.body.innerText;
  const lines = allText.split('\n');
  const results = [];
  let currentDate = '';
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.match(/June\s+\d+/i) || trimmed.match(/\d+\s+June/i)) {
      currentDate = trimmed;
      results.push('=== ' + trimmed + ' ===');
    }
    if (trimmed.match(/^[A-Za-z\s]+\d+\s*[-–]\s*\d+\s+[A-Za-z\s]+$/)) {
      results.push(trimmed);
    }
  }
  return results.join('\n');
})()
```

4. To split by matchday or date, look for date headers in the page text and associate the following lines with that date.

**Fallback sources** (if Wikipedia is unavailable):

- ESPN scoreboard at `https://www.espn.com/soccer/scoreboard` -- works for recent results via browser
- FIFA official site -- note 1: main WWW site is JS-rendered and not suitable for text extraction; prefer Wikipedia for schedules/results. Note 2: subpages like `api.fifa.com/api/v3/calendar/matches` may work, but expect limited/missing fields in raw JSON.
- 365soccer.com -- main domain redirects to `/lander`; direct curl won't return match data unless you complete browser flow. Avoid unless you can render JS/cookies.
- 365scores -- may show 404 for subpages; try main page
- Flashscore -- aggressive bot detection via Cloudflare

**Known pitcher / class-level notes:**

- When asked for "all data about these matches and the match and have all the data you need ومباريات دور ال 16", create a structured knockout template file rather than appending a small results table to a daily summary. Keep results, upcoming fixtures, and bracket progression in a dedicated file under a logical subfolder.
- **Round of 32 classification rule:** when the user states that results after the group stage belong to the Round of 32, apply that classification unconditionally. Do not ask for confirmation before classifying or writing.

- `web_search` and `web_extract` often fail when FIRECRAWL_API_KEY is unset. Default to browser.
- Google blocks automated searches with CAPTCHA. Go to Wikipedia directly.
- ESPN sub-pages may return 404; the main scoreboard page works.
- Large tournament pages (over 8000 chars snapshot) need browser_console JS extraction instead of snapshot.
- Regional sports sites: FilGoal 404s on deep links, YallaKora domain may be parked.
- **FIFA.com bot detection:** `fifa.com/en/tournaments/.../matches` returns `"Come on referee, you weren't supposed to see this!"` when accessed via browser automation. Do NOT retry — go directly to Wikipedia instead. This is expected, not a transient failure.
- **Patching a vault results file can fail when `old_string` appears more than once.** Fix: include surrounding lines in `old_string` to make it unique, or use `replace_all=true` when the change applies everywhere.
- **Inconsistent formatting in existing vault files** (double pipes, mixed indentation) can make exact-match patches brittle. Before patching, `read_file` the target section(s) to confirm the exact string on disk.
- **replace_all=true is dangerous on files with duplicated table structures.** If the file has multiple group standings with identical format (same header rows), `replace_all` will replace ALL tables with the same content. ALWAYS verify what sections match before using it. Safer: include a unique group label line in `old_string` to scope the patch to one table.

### 3. Format results

Use concise markdown tables with the user's preferred style:

- Flag emojis for teams (flags extracted from team names)
- Bold scores
- checkmark for completed, clock for upcoming
- All times in user's local timezone (UTC+3 for users in Cairo)

**Results table format:**

```
|| اليوم | المجموعة | المباراة | النتيجة | الحالة |
||------|---------|---------|---------|--------|
||| 21 июня | G | Belgium vs Iran | **0-0** | done |
```

**Statistics summary line:**

Stats: N matches completed, X goals, average Y goals per match.

### 4. Write to vault

- Check if a tournament file already exists at the expected path (see Vault paths below).
- If it exists: use `patch` (old_string/new_string) to update specific sections. Never overwrite the entire file.
- If new: use `write_file` with full structure.

**When patching an existing file, update these sections:**

- The "last updated" timestamp line
- Append new result rows to the results table
- Update the statistics section
- Update the schedule section (change clock icons to actual results for completed matches)
- Update group standings tables if standings data was extracted
- Fix incorrect data from prior versions if Wikipedia has corrected them

### Vault paths

Tournament files live in the user's second-brain vault.

- Hatem's vault: `/home/hatem/Documents/Hatem Nad/01-Projects/World Cup 2026.md`
- Hafsa vault primary file: `📚 Knowledge/World Cup 2026.md`
- Hafsa vault knockout template: `📚 Knowledge/World Cup 2026/Knockout Stage.md`
- Always check if the file exists before writing. If multiple tournament files exist, pick the one with the most recent content.

**OODA Vault note:** vaults now use numbered folders: `00-Inbox/`, `01-Projects/`, `02-Knowledge/`, `03-Archive/`, `04-System/`. Patches and reads should use the new paths.

## Reference files

- `references/vault-paths.md` -- canonical vault file paths, known score sources, and site availability notes
- `references/world-cup-2026-bracket-extraction.md` -- knockout bracket extraction notes for Wikipedia tournament pages, including known June 29 Round of 32 matchups and pitfalls with merged roster/bracket tables
- `references/round-of-16-creation.md` -- recommended sequence for building R16 brackets from completed group-stage/R32 results, including vault paths and pending-match notation rules

## User preferences

- Output in Arabic (Egyptian dialect) for sports content
- Use flag emojis for all national teams
- Concise tables, no numbered lists
- Include both results AND fixtures in the same file
- Show match times in user's local timezone: **Cairo summer time (UTC+3)**
- Update dates per user-provided "today", not system date
- Keep group standings accurate when user says "team played only 2 matches"
- Do not replace standings/tables with fabricated or partially inferred data. If source extraction is incomplete, preserve existing correct rows instead of guessing.
- For Egypt-specific World Cup facts/schedule, use `365soccer.com` as an approved supplementary source. If its WWW homepage redirects in terminal/browser, fall back to Wikipedia + FIFA match references.
- **Proactive execution:** when the user says "you do it" or gives similar terse approval, continue immediately without asking questions. Do not pause for clarification unless there is genuine ambiguity that blocks progress.
- **Post-group classification rule:** all knockout-stage matches immediately after the group phase are Round of 32 matches unless/until specific confirmed bracket data shows otherwise. Do not require explicit confirmation for this classification.
- **Direct result entry:** when the user supplies a match result inline, treat it as authoritative and patch the tournament file immediately with that exact score. Do not ask for confirmation before writing user-stated scores.
- **Bracket-first sequencing:** when the user asks to create round-of-16 matches, first update the main knockout stage file with advanced teams/TBD opponents, then spawn individual match-page files. Do not create match files before the bracket table reflects the new matchups.
- **Pending-match notation:** for round-of-16 opponents whose round-of-32 match is still ongoing, use `Team A / Team B` format in both the bracket table and individual match files, with a note that the result is pending.
- **User-supplied matchup override:** when the user states a specific World Cup matchup directly, record it as a confirmed user-supplied matchup immediately. Do not silently overwrite it with generic/placeholder opponents; if it conflicts with expected bracket logic, note the upstream R32 winner whose path is affected and update both the bracket table and the match page accordingly.

## Routing rule (authoritative over fallback order)
1. Wikipedia official pages first (Group/Round pages + knockout stage pages).
2. FIFA match references cited inside Wikipedia pages as a secondary confirmation source.
3. 365soccer.com for Egypt-specific World Cup content if user requests it.
4. ESPN scoreboard for generic/live results when Wikipedia is stale.
5. Treat FIFA main WWW site as JS-rendered; don't use it as a primary fetch target without browser execution.

## Pitfalls

- Same-group teams cannot meet in the Round of 32. If a proposed bracket entry pairs two teams from the same group, flag it as definitely wrong and do not write it.
- Knockout matchups and times come from the tournament’s canonical bracket (preferred source: Wikipedia). When group standings change, regenerate knockout entries from the bracket rather than hand-authoring team codes.
- When patching tournament tables, include enough surrounding context in `old_string` to make the match unique, especially around dates/stadiums/times that often repeat across rows.
- **Wikipedia World Cup page lag:** tournament pages may show "All statistics correct as of [yesterday's date]" even when accessed today. Always cross-check knockout results via the bracket section rather than assuming the page reflects today's completed matches.
- **Config writes:** profile-specific configs like `~/.hermes/profiles/<profile>/config.yaml` may be protected from direct patch. Use `~/.hermes/config.yaml` instead for platform integrations; that file accepts edits via `patch`.
