---
name: novel-worldbuilding-workflow
description: >
  MUST USE when the user asks to organize a novel vault/worldbuilding system in Obsidian/markdown.
  Covers: vault backup (+2 copy), worldbuilding folder structure, character/location/timeline templates,
  bridge files, chapter link blocks, and change watcher setup.
  Trigger phrases: "do backup", "make +2 copy", "هيكلة عالم", "worldbuilding", "Organize novel vault".
  NOT for: writing chapters, editing prose, deleting canonical content.
---

# Novel Worldbuilding Workflow

## When to use
- Building or restructuring a novel/wiki vault in markdown/Obsidian
- Creating worldbuilding structure: characters, locations, timeline, magic systems, religions, cultures, organizations, story notes
- Setting up bridge files from worldbuilding index to canonical files
- Adding lightweight link blocks to chapter files
- Creating a chapter change watcher

## Required sequence
1. **Backup first** — copy the vault directory to `<name>+2` before any structural changes.
2. **Create worldbuilding root** — `/00-عالم-الرواية/` with subfolders: `01-شخصيات`, `02-أماكن`, `03-تواريخ`, `04-أنظمة-سحر`, `05-ديانات`, `06-ثقافات`, `07-منظمات`, `08-ملاحظات-كتابة`, `09-خرائط-ومراجع`.
3. **Add templates** in each subfolder under `قوالب/`. Use `references/character-profile-template.md` for character files.
4. **Cell mapping step:** before branching into many character files, build one relations file at `00-عالم-الرواية/01-شخصيات/العلاقات.md` with: family tree, alliances, enemies, relationship evolution across chapters, and writer pitfalls.
5. **Create bridge files** in worldbuilding folder for existing canonical characters/locations; use `bridges` frontmatter pointing to source files.
6. **Patch chapter files** — add lightweight link block near top, after frontmatter if present. Do NOT edit prose.
7. **Add watcher** — create a small script in `09-خرائط-ومراجع/` that hashes chapter files and reports diffs.

## File naming conventions
- Characters: `<name>.md`
- Locations: `<name>.md`
- Timeline events: `<name>.md`
- Templates: `قالب-<type>.md`

## Frontmatter conventions
```yaml
---
type: character|location|timeline-event|magic-system|religion|culture|organization|story-notes
status: canonical|draft
tags: [kharun, ...]
bridges:
  - "../01-شخصيات/01-شخصية-كرون"
---
```

## Bridge file pattern
Each bridge file contains:
- frontmatter with `bridges` array
- one-line pointer to full canonical file
- essential relationships as `[[wikilinks]]`
- short notes if needed

## Chapter link block pattern
Add immediately after frontmatter or at very top:
```markdown
> **Chapter Title**
>
> 🔗 [[char1]] • [[char2]] • [[location]]
>
```

## Watcher pattern
- Hash chapter files with md5
- Store state in `.novel-state` under worldbuilding folder
- Report changed/unchanged per file with timestamp
- Keep script read-only; no edits to chapters

## Pitfalls
- Do NOT move canonical files; use bridge references instead.
- Do NOT edit chapter prose; only add link blocks.
- Do NOT delete content; move to archive if needed.
- Do NOT create duplicate active cron jobs for same reminder; keep one canonical job per reminder type.
