# Vault Duplicate Detection

## Recurring pattern: duplicate profile files across sections
A frequent duplication issue in the 8-folder structure is that persona/profile files are created in both `00-People/` and a knowledge subfolder such as `06-Knowledge/01-About/`.

## Detection method
1. Scan new/modified files after running the daily `find -newer` sweep.
2. Look for files with matching base names across `00-People/` and `06-Knowledge/*/`.
3. Compare sizes and last-modified timestamps. The newer file usually contains the canonical version.

## Merge strategy
- Treat `00-People/` as the canonical location for identity files.
- Keep the version with richer/more recent content.
- Update wikilinks in related notes instead of duplicating content.
- Do NOT delete the duplicate; either leave it as-is or update it to a stub that links to the canonical file.

## Example caught 2026-06-29
- `/home/hatem/Documents/Hatem Nad/00-People/Hatem_Shindy.md`
- `/home/hatem/Documents/Hatem Nad/06-Knowledge/01-About/Hatem_Shindy.md`
Both files were identical (same content, likely copied). Canonical location is `00-People/Hatem_Shindy.md`.

## Novel exception
Never merge or edit files under `رواية-كرون/` without explicit user request; those are guarded by boundary rules.
