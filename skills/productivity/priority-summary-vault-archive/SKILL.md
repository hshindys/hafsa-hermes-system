---
name: priority-summary-vault-archive
description: "Summarize external content (YouTube videos, repos, articles) and produce a priority-ranked brief mapped to the user's known projects, then optionally archive the result into the user's Obsidian vault."
platforms: [linux, macos, windows]
---

# Priority Summary + Vault Archive

## When to use
Use when the user asks to:
- summarize and rank by importance / priority
- produce a brief tied to their projects
- save a summary into their vault
- convert external content into actionable, project-mapped output

Applies to: YouTube videos, repositories, articles, web pages, research docs.

## Standing rules
1. **Try transcript first**, then chapters, then page metadata.
2. **Rank by user context**: map items to the user's known projects/people/dates before assigning priority.
3. **Archive on request**: when saving, write to `02-Projects/YouTube-Summaries/YYYY-MM-DD-<slug>.md` or the vault's equivalent active projects folder.
4. **No fabricated detail**: if transcript/chapters are unavailable, say so explicitly instead of inventing quotes.

## Workflow
1. **Extract** content from the source.
2. **Structure** as summary + priority table + actionable suggestions.
3. **Map to user's vault/projects**.
4. **Archive** if asked.