# Pre-Migration Safety Checklist

Before any file move in a git-tracked vault:

1. **Check git status** — `git status --short`
2. **Ensure clean working tree** — commit or stash changes first
3. **Create new folders** — `mkdir -p {00-Inbox,01-Projects,02-Knowledge,03-Archive,04-System}`
4. **Move in small batches** — don't `mv` everything at once
5. **Verify after each batch** — `find . -maxdepth 1 | sort`
6. **If accidental deletion** — `git restore --staged . && git restore .` IMMEDIATELY
7. **Commit only when clean** — `git add -A && git commit -m "refactor: ..."`

## Recovery commands
```bash
# Undo last move (files still in git index)
git restore --staged .
git restore .

# Check what was deleted
git status --short | grep "^D"

# Recover specific file
git checkout HEAD -- path/to/file.md
```
