# Vault Health Check — Daily Index Audit

## Trigger
Scheduled cron job (daily 7:00 AM) or on-demand when user asks "فحص صحة الخزنة".

## What it does
1. Reads the main index file of each vault
2. Scans actual filesystem for all `.md` files
3. Compares actual files vs indexed files
4. Updates indexes with any new files
5. Produces a status report

## Vault Paths
- **Hafsa**: `/home/hatem/Documents/Hafsa/`
- **Hatem Nad**: `/home/hatem/Documents/Hatem Nad/` (note: space in name!)

## Index Files
| Vault | Main Index | Router |
|-------|-----------|--------|
| Hafsa | `📌 Index.md` | `CLAUDE.md` |
| Hatem Nad | `04-System/INDEX.md` | `04-System/00-فهرس-الخزنة.md` |

## Step-by-Step Procedure

### 1. Read both index files
```
read_file("/home/hatem/Documents/Hafsa/📌 Index.md")
read_file("/home/hatem/Documents/Hatem Nad/04-System/INDEX.md")
```

### 2. Scan actual files
```bash
# Hafsa
find "/home/hatem/Documents/Hafsa" -name "*.md" -not -path "*/.git/*" | sort

# Hatem Nad (exclude archive)
find "/home/hatem/Documents/Hatem Nad" -name "*.md" -not -path "*/.git/*" -not -path "*/03-Archive/*" | sort
```

### 3. Find new files (not in index)
Compare file list against index entries. New files typically appear in:
- New directories (e.g., `AI-News-Sweep/`, `Music/`, `cron/`)
- New knowledge files in existing directories
- New project sub-files

### 4. Update indexes
Use `patch` (mode=replace) to add new entries to the appropriate section:
- Match the existing table format exactly
- Add rows for new files
- Update the date stamp at top of file
- Update statistics counts

### 5. Update CLAUDE.md router
If new top-level directories were added, update the vault listing in `~/Documents/Hafsa/CLAUDE.md`.

### 6. Produce report
Format:
```
📋 تقرير صحة الخزنات — [date]
✅ خزنة حفصة: [file count] — سليمة
✅ خزنة حاتم: [file count] — سليمة
📝 التغييرات: [list of new files added to index]
```

## Pitfalls

### Spaces in directory names
`/home/hatem/Documents/Hatem Nad/` has a space. Always quote paths in shell commands:
```bash
# WRONG
find /home/hatem/Documents/Hatem Nad -name "*.md"

# RIGHT
find "/home/hatem/Documents/Hatem Nad" -name "*.md"
```

### Multiple index files
Hatem Nad has several index files. The main one is `04-System/INDEX.md`. There's also `04-System/00-فهرس-الخزنة.md` (comprehensive). Update both.

### execute_code blocked in cron
`execute_code` is blocked in cron jobs. Use `terminal` for shell commands and `patch`/`read_file` for file operations.

### Duplicate footer lines
When patching the end of a file, check for duplicate footer lines that may have been created by previous patches.

### Large vault subdirectories
`AI-Skills-Research/` is ~795MB and contains hundreds of files. It's noted as a separate system in the index — don't try to enumerate all files in it.

## Statistics Tracking
| Date | Hafsa Files | Hatem Nad Files | Notes |
|------|-------------|-----------------|-------|
| 2026-06-25 | ~320+ | ~148+ | Added AI-News-Sweep, Music, OpenLore, World Cuisine (15 cuisines) |
