# Kron Vault Cleanup Workflow
## Goal
Remove duplicate filenames, numbering collisions, and parallel stale copies from a novel vault without losing data.

## Procedure
1. Run audit:
```bash
python3 /path/to/vault_audit.py "/home/hatem/Documents/مسودة كرون/" > /tmp/kron_vault_audit.md
```

2. Inspect categories in order:
- secrets → remove from vault immediately if any
- parallel folder systems → confirm whether intentional or stale
- duplicate filenames → keep canonical, archive others
- numbering collisions → renumber or archive depending on canonical choice

3. Archive duplicates:
```bash
mkdir -p "/home/hatem/Documents/مسودة كرون/أرشيف-تنظيف/2026-07-09"
mv <duplicate> "/home/hatem/Documents/مسودة كرون/أرشيف-تنظيف/2026-07-09/"
```

4. Re-run audit and confirm:
- duplicate filenames = 0 in active paths
- numbering collisions = 0 in active paths
- archived copies may still collide internally; that's acceptable since they're outside the writing read path

5. Update Queen files:
- continuity-log.md must reflect only facts actually written in drafted chapters
- jinn-rules.md / plot-outline.md pulled from CLAUDE.md / existing canonical docs only

## Decision Rules
- Never delete. Only move to `أرشيف-تنظيف/<date>/`.
- If two files share the same basename and folder, decide canonical by: frontmatter status `canonical` > completeness > creation date.
- If numbering collides, prefer the file whose content is richer/longer as canonical; archive shorter/older.
