---
title: Novel Vault Sync — Hafsa to Hatem Nad
last_updated: 2026-06-25
---

# Novel Vault Sync Pattern

## Scenario
User has a novel project (كرون) that exists in Hafsa vault (`🎯 المشاريع/رواية-كرون/`) and needs to be synced to Hatem Nad vault (`رواية-كرون/`).

## Source vs Target

| Vault | Path | Role |
|-------|------|------|
| **Hafsa** (source) | `~/Documents/Hafsa/🎯 المشاريع/رواية-كرون/رواية-كرون/` | Working copy, edited by AI |
| **Hatem Nad** (target) | `~/Documents/Hatem Nad/رواية-كرون/03-Archive/رواية-كرون/` | Archive/backup |

## Sync Procedure

1. **Copy modified files only** — don't overwrite everything
2. **Use archive folder in target** — prevents accidental data loss
3. **Preserve Obsidian frontmatter** — title, type, tags
4. **Preserve wikilinks** — `[[character]]` syntax
5. **Confirm after copy** — list what was transferred

### Example:
```bash
cp "/home/hatem/Documents/Hafsa/🎯 المشاريع/رواية-كرون/رواية-كرون/04-الفصول/الفصل-الأول.md" \
   "/home/hatem/Documents/Hatem Nad/رواية-كرون/03-Archive/رواية-كرون/04-الفصول/الفصل-الأول.md"
```

## Pitfalls
1. **Don't overwrite original in target** — always use archive subfolder for incoming files
2. **Don't use `mv`** — use `cp` to preserve source
3. **Check frontmatter** — ensure Obsidian-compatible YAML is present
4. **Verify after copy** — read the target file to confirm

## Lore Corrections Log
When user corrects novel lore, update BOTH:
1. The chapter file (frontmatter + content)
2. The character file (relationships, family links)
3. The character-map reference in novel-writing skill

### 2026-06-25 Corrections:
- كرون = ابن تارك ورتون (not standalone hero)
- نورك = بنت نومن (not هروس/creature)
- نومن doesn't know كرون yet (first meeting in Chapter 2)
- Added Scene 7: رسول نومن arrives at تارك's house
