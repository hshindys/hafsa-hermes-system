---
name: vault-restructuring
description: "OODA-based vault restructuring — organize any vault into 00-Inbox, 01-Projects, 02-Knowledge, 03-Archive, 04-System. Apply to Obsidian, filesystem, and custom vaults. MUST read before any bulk file move inside a git-tracked vault."
triggers:
  - "reorganize vault"
  - "vault structure"
  - "OODA vault"
  - "restructure files"
  - "organize folder"
  - "vault cleanup"
  - "file reorganization"
---

# Vault Restructuring — Second Brain / OODA Pattern

## When to use
- User asks to reorganize/clean up a vault, project folder, or file collection
- Vault has accumulated files in flat structure or inconsistent legacy folders/moji folders
- Setting up a new vault that needs a proven structure
- User mentions "OODA", "Infinite Brain", "Second Brain", "organize my files", "دماغ رقمي", "دماغ ثاني"
- User asks to apply the same 8-folder Second Brain structure across multiple vaults

## The Second Brain Vault Structure

Preferred layout when the user asks for a Second Brain implementation:

```
vault-root/
├── 00-People/      — Person files (family, contacts, teammates)
├── 01-Projects/    — Active projects with deliverables and context
├── 02-Decisions/   — Past decisions, alternatives, outcomes
├── 03-Companies/   — Companies, competitors, market research
├── 04-Meetings/    — Meeting notes, decisions, commitments
├── 05-Daily/       — Daily 3-5 line summaries
├── 06-Knowledge/   — Ideas, frameworks, quotes, reusable notes
└── 07-MOC/         — Maps of Content: topic summaries linking scattered notes
```

Keep separate vault folders as-is when they represent intentional projects with their own README/manifest (do not overflatten them). For user-facing renames, prefer emoji-free paths to reduce shell/encoding breakage.

### Migration from legacy folders
Common legacy names and their targets:
- `👥 / People / الأشخاص` → `00-People/`
- `🎯 Projects / المشاريع` → `01-Projects/`
- `📅 Daily / اليوميات` → `05-Daily/`
- `💡 Ideas / الأفكار` → `06-Knowledge/` or `07-MOC/`
- `🧠 Knowledge / المعرفة` → `06-Knowledge/`
- `@username/` or profile folders → `00-People/<name>.md`
- `AI-*`, `Music`, `Food`, `World Cuisine` → consider moving only content, not whole folder trees

## Alternative: New-vault clone + link rewrite
When the source vault is very messy, the user may prefer a brand-new vault over in-place restructuring. This is a safe, low-risk alternative when:
- The user explicitly asks for a *new* vault with a different name
- The source has duplicated folders/files across multiple legacy trees
- Fixing all internal wikilinks in-place would require many brittle path rewrites

Workflow:
1. Create destination vault with the desired clean structure
2. Copy canonical content into it (do *not* copy known-junk folders like `06-闽`, `.trash`, emoji-only stubs)
3. Dedup by filename: if both source trees contain the same canonical file, copy only from the authoritative tree
4. Rewrite broken wikilinks in bulk with a script: replace old path prefixes with new ones
5. Verify zero remaining old-path links with `search_files` or `grep -r '[[old-prefix'`
6. Leave the source vault untouched until the user explicitly approves removal

## Alternative STRUCTURES

### PARA/PCM
Preferred when the user explicitly cites Tiago Forte, PARA, or "بناء دماغ ثاني":
- `/01-Projects/` — active deliverables
- `/02-Areas/` — ongoing responsibilities
- `/03-Resources/` — reference/knowledge
- `/Archive/` — completed/legacy
Keep project-specific trees under the project folder; do not overflatten.
Session example: `references/para-pcm-restructure.md`.

## Verification: Finding broken wikilinks after a move
Use targeted searches for old path prefixes inside the new vault:
```bash
grep -rn '\\[\\[old-folder-prefix/' /new-vault/
```
For Arabic/emoji vaults, prioritize searching the index/hub file first — it usually contains the densest link graph. Always re-search after each batch rewrite until hits reach zero.

## Preferred Move Methods (ordered)
1. `mcp_filesystem_move_file` — preferred when parent exists and MCP server is healthy
2. Python `shutil.move` + `Pathlib` iteration — safer than shell globbing for Arabic/emoji paths; use existence checks before every move
3. Shell `mv` — only for massive batches with proper quoting; avoid `2>/dev/null` on every line

## Step-by-Step Workflow

### 1. Audit (Observe)
```bash
# List current structure
find <vault-root> -maxdepth 2 -type d | sort
# Check git status first!
cd <vault-root> && git status --short
```

### 2. Create new structure
```bash
mkdir -p {00-Inbox,01-Projects,02-Knowledge,03-Archive,04-System}
```

### 3. Move files (Act)
- Move active work → `01-Projects/`
- Move reference material → `02-Knowledge/`
- Move completed/legacy → `03-Archive/`
- Move router/index/rules → `04-System/`
- **NEVER delete** — when in doubt, archive

### 4. Index (Orient)
Create `04-System/Vault-Index.md` mapping old → new locations.

### 5. Commit (Decide + Act)
```bash
git add -A
git commit -m "refactor: OODA vault structure"
```

## CRITICAL PITFALLS

### Git safety
**ALWAYS** check `git status` before moving files in a git-tracked vault.
If you accidentally delete files from working directory:
```bash
git restore --staged .
git restore .
```
This recovers them from the index immediately.

### MCP filesystem server failures
When `mcp_filesystem_move_file` fails with "MCP server unreachable":
- **DO NOT retry** — wait ~60s between retries
- **Fallback to terminal**: `mv "source" "destination"`
- Batch moves in single `terminal()` calls for efficiency

### Encoding issues with non-ASCII paths
Arabic/emoji folder names break in some shells. Use `mv` via terminal with proper quoting:
```bash
mv "/path/with arabic" "/new/path"
```
If `mv: cannot stat` — the file may have been moved already or encoding mismatch. Check with `find` first.

### Duplicate detection
After moving files, check for duplicates:
```bash
# If file exists in both old and new location, remove from new
rm -rf "/new/path/duplicate-folder"
```

## Pitfalls & Real-World Lessons

### Emoji folders create hidden duplicates during copy/move
When a vault uses emoji-prefixed folder names (`👥 الأشخاص`, `🧠 المعرفة`, `💡 الأفكار`), naive `cp -a` or `mv` with globbing can silently fail because of encoding. The result: a second pass creates folders suffixed with `_emoji` or `_old`. **Always inspect the folder tree after each batch move**, not just the file count.

### Multiple-pass copy/move strategy for emoji vaults
For large reorganizations with emoji names:
1. First overwrite missing files with `cp`/`mv` into the target
2. Remove the source tree completely (`rm -rf src`)
3. Verify with `find` — do NOT trust file counts alone

### Orphan-list path mismatch
When `find_orphans` returns human-friendly paths with cleaned emoji/spaces (e.g., `Arius.md`) but the actual canonical files live under legacy folders (e.g., `📚 World of Kron/Characters/Arius.md`), **do not bulk archive by the orphan display name**. That mismatch causes `mv` to fail with ENOENT and can leave the vault inconsistent. Fix order:
1. Run `find . -name '<display name>'` to confirm real paths
2. Move only confirmed existing paths
3. Re-run `find_orphans` to verify cleanup; if display names persist, mark them manually in index/readme instead of shell moves

### Batch-move failures with unknown paths
If `mv`/`git mv` returns `request failed: status=404` or `ENOENT` during a bulk move, the source was renamed/moved in an earlier pass or does not exist. **Do not rerun the same bulk command.** Use a narrow search to locate remaining candidates and move them individually.

### MCP filesystem server failures
When `mcp_filesystem_move_file` fails with "MCP server unreachable":
- **DO NOT retry** — wait ~60s between retries
- **Fallback to terminal**: `mv "source" "destination"` with proper quoting for emoji/arabic paths
- Batch moves in single `terminal()` calls for efficiency

### Multiple-pass move strategy
For large reorganizations (>100 files), do NOT try to move everything in one bash command with `2>/dev/null` suppressions — errors get hidden and you miss what didn't move. Instead:
1. **First pass:** move top-level categories to OODA folders (suppress errors)
2. **Verify:** check what landed correctly vs what got nested
3. **Second pass:** flatten any nested structures with explicit `mv` per subfolder
4. **Final audit:** compare old file list to new file list

### Cleanup of old empty directories
After all moves complete, remove old category directories that are now empty:
```bash
rmdir "/path/to/old-dir" 2>/dev/null  # rmdir only removes empty dirs (safer than rm -rf)
```

### Post-move git commit
Once structure is verified, commit immediately so the new state is the recovery point:
```bash
cd <vault-root>
git add -A
git commit -m "refactor: OODA vault structure"
```
If everything is committed, future mistakes are always reversible via `git restore`.

## Verification
After restructuring:
```bash
# Confirm clean root (only OODA folders + config files)
find <vault-root> -maxdepth 1 -not -name ".git" -not -name ".obsidian" | sort
# Confirm no data loss
git status --short
# Confirm no unintended nesting
find <vault-root>/00-* <vault-root>/01-* <vault-root>/02-* -name "SKILL.md" -maxdepth 2 | sort
```

## What NOT to do (lessons from 2026-06-24 session)
1. **Never batch-move files with `2>/dev/null` on every line** — you'll miss critical errors
2. **Never `rm -rf` files you're reorganizing** — always `mv` to archive, git is your safety net
3. **Never assume a move succeeded** — always verify with `find` after each batch
4. **Never keep duplicate files in both old and new locations** — the old copy creates confusion about which is canonical
5. **If `git` is the VCS, commit BEFORE starting** — so `git restore .` can undo everything if the reorg goes wrong

## References
- `references/oda-loop-concept.md` — OODA loop theory from Infinite Brain video
- `references/migration-checklist.md` — Pre-migration safety checklist
