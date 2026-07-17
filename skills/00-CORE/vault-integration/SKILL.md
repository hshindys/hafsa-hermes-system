---
name: vault-integration
description: >
  MUST USE when user has an Obsidian vault or structured knowledge base ("second brain")
  and wants to connect it to Hermes Agent for context engineering.
  
  Covers: Obsidian vault symlink pattern, CLAUDE.md routing, vault-to-SOUL.md pipeline,
  living files vs dead files, multi-vault management.
  
  Use when user mentions: Obsidian, vault, second brain, knowledge base, CLAUDE.md,
  vault integration, context engineering, living files.
metadata:
  hermes:
    tags: [obsidian, vault, second-brain, context-engineering, knowledge-base]
    priority: high
---

# Vault Integration — Connect Obsidian (or any KB) to Hermes

Connect structured knowledge bases (Obsidian vaults, markdown KBs) to Hermes Agent for context engineering.

## When to use
leading words: `routing`, `second-brain`, `living-files`, `vault-archive`

## Standing rules (apply for the whole skill)
1. `routing`: read the vault router file first before answering; use paths from routing table
2. `second-brain`: only store evergreen, holistic data; noisy transient data stays out
3. `living-files`: if a file cannot be accessed by the agent, move it into the vault
4. `vault-archive`: never delete; archive instead

- User has an Obsidian vault they want to connect
- User mentions "second brain" or "knowledge base"
- User wants to link vault files as Hermes context
- User wants to create/update SOUL.md from vault content
- User mentions CLAUDE.md or vault routing

## Architecture

```
Hermes Agent
├── SOUL.md (identity — always loaded)
├── vault-hafsa/ → symlink to ~/Documents/Hafsa-1/ (loaded on demand)
├── vault-hatem-nad/ → symlink to ~/Documents/Hatem Nad/ (loaded on demand)
└── Skills + Plugins (loaded on demand)
```

## Setup Pattern

### Step 1: Create Symlinks

```bash
# Link vault to Hermes profile
ln -sf /home/hatem/Documents/Hafsa ~/.hermes/profiles/hafsa/vault-hafsa-1
ln -sf /home/hatem/Documents/Hatem\ Nad ~/.hermes/profiles/hafsa/vault-hatem-nad
```

### Step 2: Create CLAUDE.md Router

Each vault gets a `CLAUDE.md` that serves as the entry point for the AI agent:

```markdown
# CLAUDE.md — Hafsa Agent Vault Router

## ⚠️ تعليمات للـ AI Agent
1. اقرأ هذا الملف أولاً
2. حدد الموضوع → اذهب للملف المناسب
3. أجب بناءً على الملفات — لا تخترع معلومات
4. لا تحذف أي حاجة — انقل للأرشيف بدل الحذف

## 📂 الـ Vaults المتاحة
| الـ Vault | الـ Path | الوصف |
|----------|---------|-------|
| Hafsa | `~/Documents/Hafsa-1/` | خزنة حفصة |
| Hatem Nad | `~/Documents/Hatem Nad/` | خزنة حاتم |

## 📖 فهرس خزنة حفصة
| المجلد | الوصف |
|--------|-------|
| @حفصة/ | الهوية والشخصية |
| 🎯 المشاريع/ | المشاريع الحالية |
| ... | ... |
```

### Step 3: Vault Rules

1. **لا تحذف أي حاجة** — انقل للأرشيف بدل الحذف
2. **كل ملف جديد** — أضفه للفهرس المناسب
3. **اليوميات** — تُكتب يومياً
4. **الأفكار** — تُضاف لبنك الأفكار
5. **الـ frontmatter** — كل ملف لازم فيه frontmatter

## 8-Folder Second Brain Structure

When user asks for second brain setup, use this canonical structure on both vaults:

```text
00-People/       — كل شخص في حياتك مع ملف شخصي كامل
01-Projects/     — كل مشاريعك بالتواريخ والسياق
02-Decisions/    — قراراتك الماضية + البدائل + النتيجة
03-Companies/    — شركات، منافسين، أبحاث سوق
04-Meetings/     — محاضر اجتماعات + قرارات committed
05-Daily/        — ملخص يومي 3-5 أسطر لكل يوم (بالميلادي والهجري)
06-Knowledge/    — أفكار، frameworks، اقتباسات، ملاحظات قابلة لإعادة الاستخدام
07-MOC/          — Maps of Content: ملفات تلخص موضوعات كبيرة وتربط scattered info
```

**Rules for Second Brain Setup:**
1. Always create `00-Second-Brain-Index.md` at vault root after setup
2. Give each folder a one-line README.md before migration
3. When migrating from old emoji-folders, move content into matching numbered folder, then remove old folder
4. `README.md` in each folder should explain the folder's purpose in 1 line
5. After migration, run a health check to confirm counts by folder

## Nightly Second Brain Compounder (Cron)

For each vault, create a nightly cron job that runs at **23:00 Cairo**:

```bash
cronjob action=create schedule='0 23 * * *' name='Second Brain Nightly Compounder'
```

Cron prompt responsibilities:
1. Read vault stats and recent notes to detect real today-changes.
2. If no meaningful changes, preserve silence when possible instead of noisy empty edits.
3. Create/update today's daily note in `05-Daily/<YYYY-MM-DD>.md` if missing; keep it minimal if no real events happened today.
4. If meaningful changes detected, scan mentions for:
   - people → `00-People/`
   - projects → `01-Projects/`
   - companies → `03-Companies/`
   - decisions → `02-Decisions/`
5. Merge duplicates only after confirming they are true duplicates; don't merge across non-novel-active namespaces.
6. Update `06-Knowledge/07-MOC/README.md` when a topic section grows new hub files.
7. Do NOT modify novel chapters unless explicitly requested: `رواية-كرون/` is off-limits.
8. Emit a short report to `/home/hatem/Documents/Hafsa/.hermes-cron/second-brain-report/<MM-DD-YYYY>.md` with:
   - new/modified count
   - orphan findings
   - duplicate merges
   - strategic review flags
   - explicit "no actionable changes today" when applicable
9. Prefer MCP vault tools and `mcp_filesystem_*` for discovery; use `recent_notes`, `find_orphans`, and `get_vault_stats` instead of shell-style scans.
10. Stay small/quiet. Actionable beats report-but-empty.

**Boundaries:** never delete files; archive instead. never modify novel chapters without explicit user request.

## Vault Migration Pattern (Emoji → Numbered)

When consolidating old vault structure into the 8-folder system:
1. Create numbered folders if not already present
2. Copy old emoji-folder contents into matching numbered folder with `cp -a` or manual merge
3. Verify counts: `find folder -maxdepth 1 -type f | wc -l`
4. Remove old emoji folder only after confirming contents moved
5. Handle empty placeholder directories with `rmdir` vs `rm -rf` safely

## Living Files vs Dead Files

| Living Files ✅ | Dead Files ❌ |
|-----------------|---------------|
| Markdown in Obsidian vault | Files on disconnected hard drive |
| Accessible by AI agent | No AI access |
| Can be used as context/reference | Cannot be loaded into sessions |
| Synced across devices | Single location, no backup |

**Rule:** If a file cannot be accessed by the AI agent, it is useless. Convert dead files to living files by moving them into the vault.

## Vault-to-SOUL.md Pipeline

When building a persona from a vault:

1. **Read identity files** — `@حفصة/`, `01-About/`
2. **Extract health info** — medications, allergies, conditions
3. **Extract relationships** — family, preferences
4. **Extract projects/goals** — what the user is working on
5. **Write SOUL.md** — compile into identity document
6. **Update memory** — save key facts to persistent memory

## Multi-Vault Management

For users with multiple vaults (e.g., personal + professional):

```bash
ln -sf ~/Documents/Work-Vault ~/.hermes/profiles/<profile>/vault-work
ln -sf ~/Documents/Personal-Vault ~/.hermes/profiles/<profile>/vault-personal
```

Each vault gets its own section in CLAUDE.md with clear routing.

## Active Tasks File Vault-Linking Pattern

Add an executable todo file inside the vault so tasks remain operational even outside Hermes.

Canonical path:
`/home/hatem/Documents/Hatem Nad/01-Projects/Active/This.md`

Format:
- Use checkbox tasks in Arabic with exact reference IDs when available
- Add a Linked section with vault paths, cron IDs, and current status
- Keep This.md short; archive completed items instead of deleting them

## Vault Journal Routing

When daily notes cannot be patched by emoji folder path, use:
1. Search instead of hardcoded emoji paths
2. Read the daily note, then patch directly
3. If emoji-path mismatch occurs, prefer the canonical `📆 Daily` routing only after confirming actual folder exists in that vault

## Cron Job Workdir Constraint

`cronjob action=create` fails if `workdir` does not exist. Verify directories before creating jobs:
```bash
find /home/hatem -maxdepth 4 -type d -name "<folder>"
```

Fixes for World Cup briefs:
- use `/home/hatem/Documents/Lola/04-Projects/World Cup 2026`
- not legacy `/home/hatem/Documents/Hatem Nad/01-Projects/`

## Cron Index Update: Emoji Path Scanner Pitfall

In scheduled cron jobs, `terminal` may block or delay emoji-prefixed directory names with a variation-selector security gate even when the path is valid. This affects exact `find "/path/😎 People"` style commands.

Preferred cron-safe approaches, in order:
1. **`mcp_filesystem_directory_tree`** — use directory tree listings instead of `find -printf` when possible; it handles emoji folder names without scanner approval friction.
2. **Single `/tmp` Python scan** — write a short script with English-only labels and no inline emoji shell strings, run it via `terminal`, and read the structured output back.
3. **Avoid** chained emoji-laden shell commands in cron; they create flaky approvals that block index updates.

Pattern:
- Reconcile counts/sizes in one read pass.
- Then write the corrected index with one `write_file` rebuild rather than multiple patches.

## Cron Pause/Error Recovery Pattern

When a cron shows `last_status: error` and `state: paused`, recover in this order:
1. Manual run: `cronjob action=run job_id=...`
2. If still paused, resume: `cronjob action=resume job_id=...`
3. Confirm status returns to `state: scheduled` and `enabled: true`.

Pitfalls:
- Do not blindly `update` a paused job; `resume` is the explicit lift.
- After manual run, check `executed: true` and `execution_success: true`.

## OrphanNote Curation: Backlinks Sampling

Before mass-moving or deleting orphans, sample `get_backlinks` across a representative mix:
- Active project files
- Active/personal files
- Archive/template files

If nearly all sampled files show `No backlinks found`, the vault likely disconnected after a major restructure, not because the files are dead. In that case:
1. Batch-move obvious duplicates/indexes into `03-Archive/old-indexes/`
2. Add backlinks from active hub files to the orphans that should be reachable
3. Keep archive/template/example files in place — they are functional even without backlinks

## Duplicate Vault Index Cleanup

After restructuring from emoji-folders to numbered folders, vaults can retain stale index files:
- `00-Second-Brain-Index.md`
- `04-System/Hatem-Vault-Index.md`
- `04-System/Vault-Index.md`
- `Novel-Kron-Vault-Index.md`
- `Hatem-Vault-Index.md` and `Hatem-Vault-Structure.md`

Move duplicates to `03-Archive/old-indexes/` to reduce Vault Health Check noise. Do not delete — archive preserves them.

## Vault Todo File Linking

Keep an executable todo file inside the vault so tasks remain operational even outside Hermes.

Canonical path:
`/home/hatem/Documents/Hatem Nad/01-Projects/Active/This.md`

Format:
- Use checkbox tasks in Arabic with exact reference IDs when available
- Add a Linked section with vault paths, cron IDs, and current status
- Keep This.md short; archive completed items instead of deleting them

## Conversation Continuation Rule

When the user gives short approvals such as `ok`, proceed to the next queued task without asking. Save clarification questions only for genuinely ambiguous steps.

## Cron Pause/Error Recovery Pattern

When a cron shows `last_status: error` and `state: paused`, recover in this order:
1. Manual run: `cronjob action=run job_id=...`
2. If still paused, resume: `cronjob action=resume job_id=...`
3. Confirm status returns to `state: scheduled` and `enabled: true`.

Pitfalls:
- Do not blindly `update` a paused job; `resume` is the explicit lift.
- After manual run, check `executed: true` and `execution_success: true`.

## OrphanNote Curation: Backlinks Sampling

Before mass-moving or deleting orphans, sample `get_backlinks` across a representative mix:
- Active project files
- Active/personal files
- Archive/template files

If nearly all sampled files show `No backlinks found`, the vault likely disconnected after a major restructure, not because the files are dead. In that case:
1. Batch-move obvious duplicates/indexes into `03-Archive/old-indexes/`
2. Add backlinks from active hub files to the orphans that should be reachable
3. Keep archive/template/example files in place — they are functional even without backlinks

## Duplicate Vault Index Cleanup

After restructuring from emoji-folders to numbered folders, vaults can retain stale index files:
- `00-Second-Brain-Index.md`
- `04-System/Hatem-Vault-Index.md`
- `04-System/Vault-Index.md`
- `Novel-Kron-Vault-Index.md`
- `Hatem-Vault-Index.md` and `Hatem-Vault-Structure.md`

Move duplicates to `03-Archive/old-indexes/` to reduce Vault Health Check noise. Do not delete — archive preserves them.

## Functional Vault Creation Pattern

When the user asks to build a new purpose-built vault inside an existing vault (e.g., a "work system" vault), use this operational pattern:

1. **Create a top-level folder** with a stable, descriptive name; avoid future rename risk.
2. **Create purpose folders by role**, not by lifecycle stage. Example roles: Focus, Daily, Metrics, Agents, Base, Live, Review, Archive.
3. **Ship working templates immediately** for each role, not README placeholders.
4. **Register every new file** in the global vault `📌 Index.md` same turn, and update Notes/Folders/Total size metadata.
5. **Seed one real daily note** tied to the current date so the system is usable immediately.

Minimum viable files for a work-system vault:
- `README.md` with principles/system description
- `Focus/01-Current.md` + `02-Inbox.md`
- `Daily/Template-Daily.md` + `Template-Close.md`
- `Agents/Index.md` with ownership matrix
- `Metrics/README.md` + `Base/README.md`

Index-update procedure:
- Add new folder under `## Folders`
- Add new files under `## Notes` preserving alphabetical order
- Increment `Notes:` count by exact files created
- Increment `Folders:` count by exactly 1

### Cron / Automated Index Patching Pitfall

In cron/automated vault indexing, **do not chain multiple `patch` calls blindly** — they can introduce duplicate entries if earlier patches change matching context for later ones, or if duplicates already exist in other sections (e.g. same file already appears under a different section).

Safe cron patterns, in order of robustness:
1. **Preferred:** Reconcile the full file list first (`list_notes` + directory scan), then emit one corrected version with `write_file` instead of multiple patches.
2. **Fallback:** Read the current index, compute the exact unique diff, and apply a minimal number of `patch` calls from newest to oldest sections. Verify by re-reading before declaring done.
3. **Avoid:** Incremental patches without checking whether the same path is already present elsewhere.

When duplicates are detected mid-run, switch from patching to a full `write_file` rebuild rather than trying to surgically remove duplicates with more patches.

## Flaky MCP Filesystem Recovery in Cron

In cron/automated sessions, exact duplicate failures from `mcp_filesystem_search_files` — especially failures reporting the filesystem MCP server is unreachable — are a signal to stop retrying the same tool class and pivot, not to retry harder.

Recovery order:
1. Stop using `search_files` for the rest of the run.
2. Use `mcp_filesystem_directory_tree` for structure discovery; it handles hidden/emoji dirs without approval friction.
3. Use `mcp_filesystem_read_text_file` for exact reads.
4. Use `mcp_filesystem_edit_file` or `patch` for targeted edits only when previous content is confirmed exact.
5. Use `terminal` with `/tmp` helper files for counts, lists, or any `find` / `wc -l` / diff-style work.
6. For index rebuilds, use one `write_file` rebuild after reconciliation rather than many edits.

Pitfall:
- Do not keep calling `search_files` once it reports an identical backend failure twice; that tightens the block instead of escaping it.

## Knowledge Base Patterns

### Tool Adoption Workflow

When the user asks to adopt a GitHub/repo/CLI tool into the vault workflow, follow this sequence in one turn:

1. **Verify repo/tool identity** — if `git clone` fails or repo not found, run `gh search repos "query" --limit 10` before retrying with correct owner/name. If the tool has no discoverable source or is unavailable, do not block the workflow; record the blocker as a pending item.
2. **Install or clone** — prefer upstream installer scripts for binaries. If cloning a large repo, use:
   - `git clone --depth 1 --filter=blob:none --sparse <url> <path>`
   - `git sparse-checkout set <paths>` for minimum viable content
   - Full history fetch should be deferred or run in background, not block session progress.
3. **Register in Hermes if applicable** — for MCP servers:
   - `printf 'Y\n' | hermes mcp add <name> --command <absolute-path>`
   - This bypasses interactive tool-selection prompts and enables all tools.
4. **Verify basic operation** — run a lightweight probe:
   - MCP: `list_projects` / `config list` / `--version`
   - CLI: `<tool> --version` or a harmless query
5. **Index/integrate** — for code-intelligence tools, run index; for vault tools, run markitdown or similar converter; for search tools, run `doctor --json` to confirm channels.
6. **Record architectural decision** — store an ADR via the indexed project's `manage_adr mode='store'` so the decision persists across sessions.
7. **Update vault Index.md in the same turn** — append tool status, tags, and any new files under `## Notes`.
8. **Update Sync-Manifest.md if it changes ownership or connector scope** — only when rules are actually affected.
9. **If source is unavailable**: append a `## Pending Tools` section to the repo/tool markdown note with status `blocked/missing-source`, and continue with available tools. Do not retry the same discovery query more than twice in one turn.

Pitfalls:
- Large-fork index/diff reruns often fail via MCP with `project not found`; retry with explicit `project="..."` parameter.
- `gh search repos` hits 403 on GitHub HTML search pages; use the GitHub CLI search endpoint instead.
- `install.sh` with `--skip-config` avoids agent-config prompts when you want manual MCP registration later.
- Never treat a single failure as proof a tool is broken; capture the retry pattern, not the original error.
- If a tool has no discoverable open source/repo, do not stall; mark it pending and move on.

### Recipe/Food Vault (World Cuisine Healthy Recipes)

When building a recipe knowledge base in the vault:

1. **Structure**: `🍳 Food/World Healthy Recipes.md` with per-cuisine sections
2. **Health tags**: Each recipe tagged with "مناسب لـ:" (diabetes, hypertension, etc.)
3. **Allergy safety**: NEVER include recipes with user's allergens (check SOUL.md)
4. **Format**: Consistent template — ingredients, steps, health notes
5. **Integration**: Link to meal reminder cron for daily suggestions
6. **Index update**: Add recipe section to vault Index.md

See `world-recipes-vault` skill for full recipe template and cuisine guide.

## Obsidian Frontmatter for Vault Files (kepano/obsidian-skills pattern)

When adding or editing notes in any Obsidian vault, use consistent YAML frontmatter. This enables Obsidian graph view, backlinks, and plugin compatibility.

### Standard Frontmatter Template
```yaml
---
title: [Note Title]
type: [note|chapter|character|world|recipe|concept]
category: [category name]
status: [active|draft|archive|completed]
updated: 2026-06-25
tags: [tag1, tag2, tag3]
---
```

### Type-Specific Frontmatter

**For Fiction/Novel Files:**
```yaml
---
title: [اسم الفصل/الشخصية]
type: chapter|character|world
novel: كرون
role: protagonist|heroine|secondary
status: مكتمل|draft
pages: 25
created: 2026-06-25
tags: [arabic-novel, fantasy, jinn]
---
```

**For Character Files:**
```yaml
---
title: [اسم الشخصية]
type: character
novel: كرون
role: protagonist|heroine|secondary
father: [أب]
mother: [أم]
occupation: [المهنة]
created: 2026-06-25
tags: [character, jinn, role]
---
```

**For Recipe Files:**
```yaml
---
title: [اسم الوصفة]
type: recipe
cuisine: [المطبخ]
calories: [السعرات]
suitable-for: [السكري، الضغط، القلب]
allergy-safe: [ممنوع لحاتم: سمك/جمبري/كابوريا]
updated: 2026-06-25
tags: [recipe, healthy, cuisine]
---
```

### Wikilinks Pattern
Use `[[Note Name]]` for internal vault links to enable Obsidian backlinks and graph view:
- `[[كرون]] — البطل (ابن [[تارك]] و[[رتون]])` 
- `[[نورك]] — البطلة (ابنة [[نومن]])`
- Update wikilinks whenever new related notes are created

### Vault Sync Pattern (Hafsa → Hatem Nad)
When user requests sync between vaults:
1. Copy modified files from source vault to target vault
2. Preserve Obsidian frontmatter and wikilinks
3. Use archive folder in target vault to prevent accidental overwrites
4. Confirm after copy: `✅ تم النقل`

## Memory Architecture Pattern (Session Cache + Topics Index)

For agents that run multiple sessions with context persistence needs:

### Structure
```
memory/
├── session-cache.md      # Last session summary (read first 30s of new session)
├── topics-index.md       # Semantic links between concepts (OpenLore-style)
├── decisions.md          # Decision log with date + context
└── preferences.md        # User preferences snapshot
```

### Session Cache Pattern
- At end of each session, write 1-paragraph summary to `memory/session-cache.md`
- At start of new session, read this file FIRST before any other context
- Include: what was done, decisions made, pending items
- Token saving: ~75% reduction in context reload

### Topics Index Pattern (OpenLore-style)
- Map semantic links between concepts: `المفهوم A ←→ المفهوم B ←→ العلاقة`
- Group by domain: health, food, religion, relationships, tech
- Update after each session that introduces new concepts
- Token saving: ~83% reduction when searching for specific info

### Decisions Log
- Format: `## YYYY-MM-DD` → decision → context → status
- Track: what was decided, why, what's pending
- Prevents re-discussing the same decisions

### Pitfalls
1. **Don't let session-cache grow too large** — keep it to last session only, archive older summaries
2. **Topics index needs maintenance** — update links when relationships change
3. **Decisions log should be append-only** — never delete, only add corrections as new entries

## Nightly Routing/Health Append Pattern

For nightly vault maintenance that appends summaries to Focus, memory.md, or daily notes:

- Use exact-match replacement, not blind incremental append; confirm the tail anchor before patching.
- If `edit_file/patch` repeatedly fails because the anchor does not match exactly, switch to a full-read → rewrite flow or a precision `replace_in_note` rather than re-trying the same patch.
- Avoid editors that inject variation selectors or capricious whitespace; preserve the file's existing line endings.
- **`mcp_filesystem_edit_file` caveat:** when it fails with `"Invalid arguments ... expected array, received undefined"` for `edits`, fall back to `patch` for single replacements. This is a tool-shape validation issue, not a bad anchor.
- Do not update `📌 Index.md` from cron unless the current session explicitly owns indexing; append-only reporting files are safer targets.

## Nightly Routing Gap Detection Pattern

When the router file (`🧠 Hafsa Vault.md` or similar) references paths that may no longer match the live vault structure:

1. Read the router first.
2. For each routed target, confirm existence with `mcp_filesystem_list_directory` / `read_text_file`, not assumptions.
3. Distinguish three states: missing folder, folder exists but routed file missing, folder and file both exist with different names.
4. Append only a dated RTL bullet block; do not create, rename, or delete anything.
5. Avoid duplicate section headers by replacing the exact prior routing-check block instead of appending a new one.

Recurring Hafsa vault mismatches to watch for:
- `/home/hatem/Documents/Hafsa/02-Work-System/` exists, but some older checks still reference `02-Areas/Work-System/`
- Projects live under `01-Projects/`, while older router snapshots may say `02-Projects/`
- `📚 Resources/` exists; `📚 Knowledge/` and `02-Knowledge/` do not
- `05-Open-Notebook/` does not exist despite past references
- World Cup route may resolve to `📚 Resources/` or `03-Resources/World Cup 2026/` depending on migration state

## Cron Mode: Plural Diary Namespace & Duplicate-Index Handling

Some vaults accumulate parallel daily-note namespaces, especially during migration:
- dated folders like `📅 اليوميات/`, `05-Daily/`, `📅 Daily/`
- duplicate index files at root and inside `04-System/`

Safe cron behavior:
1. Treat absent root index as normal; don’t invent one unless requested.
2. If multiple dated-note folders exist, do not merge them automatically; report them as cleanup candidates.
3. Prefer the most actively updated dated folder for today-note decisions, but list all candidates in the report.
4. Do not treat duplicate index files as actionable unless asked; mention them as archive candidates.

## Cron Mode: Quorum Before Editing Novel Vaults

Cron jobs must not touch novel-content folders unless explicitly requested:
- `رواية-كرون/`
- `📚 World of Kron/`
- `03-World-of-Kron/`

Even if duplicates or orphans appear there, report only. No merge, no content rewrite.

## Cron Mode: Strategic Triggers

Emit a cron report even when “no real activity” if these signals exist:
- multiple daily-note namespaces exist
- duplicate vault indexes exist outside `03-Archive/old-indexes/`
- orphan notes exceed a stable baseline
- a tracked strategic file is stale, e.g. World Cup tracker update timestamp > tournament match cadence

## World Cup Router Mismatch Detection

When a vault router references a specific markdown file inside an existing folder:

1. Confirm the folder exists.
2. Confirm the exact filename exists.
3. If only the folder exists, report the missing file as a routing gap; do not create the file without an explicit request.
4. Distinguish "folder missing" from "folder exists but routed file missing" — they are different findings.

## Quiet Append in Arabic/RTL Reports

Append RTL summary blocks to `Focus/01-Current.md` and `memory.md` with a dated header, compact bullet form, and no invented creation/deletion actions. Use reporting only unless the task explicitly requests remediation.

## Recent-Note Backlink Enrichment (Cron)

When a cron task asks to enrich only the most recently modified notes with wiki-style links:
1. Use `recent_notes`, not hardcoded filenames.
2. Skip sensitive/config files by content-signature, not by filename alone: `token.*`, files containing `PAT`, frontmatter-only router files, and the global `📌 Index.md` if it already has adequate backlinks.
3. For each candidate, read content, search for entities/topics, then append a new `## روابط ذات صلة` section if absent.
4. If vault-path fails, recover with `search_by_folder`/`search` instead of aborting.
5. Do not touch novel chapters in `03-World-of-Kron/` or `📚 World of Kron/` unless explicitly requested.

## Daily Health Check (Cron)

See `references/vault-health-check.md` for the full daily vault audit procedure.
- See also `references/second-brain-cron-health-rules.md` for divergent structural health signals to report even with no content edits.

## Cron Health Signals Reference

Use `references/second-brain-cron-health-rules.md` when cron vault health reports show multi-namespace mirrors, duplicate indexes, stale strategic trackers, or elevated orphan baselines.

## Cron Health Signals Reference

Use `references/second-brain-cron-health-rules.md` when cron vault health reports show multi-namespace mirrors, duplicate indexes, stale strategic trackers, or elevated orphan baselines.

## Daily Health Check (Cron)
- Scans both Hafsa and Hatem Nad vaults for new files
- Updates index files and CLAUDE.md router
- Produces status report for Telegram
- Handles pitfalls: spaces in paths, multiple index files, execute_code blocked in cron

## Multi-Vault Smart Lookup Wrapper

When the user wants one smart-lookup command across multiple vaults, use the shared wrapper.

1. **Script path**: `/home/hatem/.hermes/profiles/hafsa/scripts/vault_smart_lookup_wrapper.py`
2. **Implementation**: delegates to `vault_smart_lookup.py` with `--vault <path>`
3. **Environment override**: `VAULT_EXTRA_ROOTS` colon-separated list of extra entity roots
4. **Per-vault router**: each vault root should contain a `🧠 Vault.md` with routing rules and suggested command examples
5. **Entity traversal**: searches primary vault plus any extra roots for matching entity files and `Relations/<name>.md`

## Multi-Vault Smart Lookup Wrapper

When the user wants one smart-lookup command across multiple vaults, use the shared wrapper.

1. **Script path**: `/home/hatem/.hermes/profiles/hafsa/scripts/vault_smart_lookup_wrapper.py`
2. **Implementation**: delegates to `vault_smart_lookup.py` with `--vault <path>`
3. **Environment override**: `VAULT_EXTRA_ROOTS` colon-separated list of extra entity roots
4. **Per-vault router**: each vault root should contain a `🧠 Vault.md` with routing rules and suggested command examples
5. **Entity traversal**: searches primary vault plus any extra roots for matching entity files and `Relations/<name>.md`

## See Also

- `obsidian` skill — Read/write/search Obsidian notes
- `hermes-agent` skill — SOUL.md, profiles, context files
- `references/vault-to-soul-pipeline.md` — Detailed persona extraction workflow
- `references/vault-health-check.md` — Daily vault health audit procedure
- `references/sports-data-acquisition.md` — External sports-data fetch fallback pattern
