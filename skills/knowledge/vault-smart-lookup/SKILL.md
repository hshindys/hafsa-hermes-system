---
name: vault-smart-lookup
description: "Vault-aware semantic search + entity traversal across multiple markdown vaults. Use when the user asks where something lives in their vault, wants relationship traversal for a person/entity, needs cross-vault search, or says 'search my vault' / 'find in Lola/Hafsa/Dina/Hatem Nad/رواية-كرون'. Default: vault-aware wrapper around the shared lookup script with explicit routing output."
tags: [vault, search, second-brain, obsidian, kg]
related_skills: [youtube-content, obsidian, obsidian-markdown, llm-wiki]
---

# Vault Smart Lookup

## When to use
- User asks for information location in any vault
- Need to traverse entity relationships in World of Kron / people / projects
- Cross-vault discovery: same operation across Hafsa/Hatem Nad/Dina/Lola/رواية-كرون
- Prefer lightweight lookup without heavy vector DB installs

## Core principle
Routing first, search second. Every vault defines:
1. A routing map from topics to folders
2. A shared lightweight lookup script path
3. An index-rebuild convention

## Shared asset
Use this wrapper for all vaults unless the user explicitly wants the raw script:
```
/home/hatem/.hermes/profiles/hafsa/scripts/vault_smart_lookup_wrapper.py
```

## Commands
```bash
# Query
python3 <wrapper> --vault "<vault path>" --query "<سؤال>"

# Entity traversal
python3 <wrapper> --vault "<vault path>" --entity "<اسم>"

# Rebuild index
python3 <wrapper> --vault "<vault path>" --query "..." --rebuild
```

## Vault map
Return as table when user asks broad questions:
- `/home/hatem/Documents/Hafsa` — medical, projects, kron, world cup, memory
- `/home/hatem/Documents/Hatem Nad` — people, projects, companies, meetings, decisions, daily, kron novel
- `/home/hatem/Documents/Dina` — projects, research, ideas, archive, daily, memory
- `/home/hatem/Documents/Lola` — agents, workflows, system config, memory, projects
- `/home/hatem/Documents/رواية-كرون` — characters, world, plot, chapters, maps, references
- `/home/hatem/Documents/Media-Project-Vault` — media project archive
- `/home/hatem/Documents/home` — home vault

## Output format
Always JSON, ranked by score with path/title. Do not paraphrase unless asked.

## If no results
1. Rebuild index with `--rebuild`
2. If still empty, inspect vault root for obvious routing files:
   - `🧠 ... Vault.md`
   - `CLAUDE.md`
   - `📌 Index.md`

## Pitfalls
- `youtube-transcript-api` or other heavy ML installs often fail with permission-denied on system Python. Use this skill’s lightweight script instead.
- Entity graph is text-match only by default; for advanced relation chains, extend Entities/Relations files instead of switching stacks.
- Do not mutate other personas’ vault files unless explicitly directed.