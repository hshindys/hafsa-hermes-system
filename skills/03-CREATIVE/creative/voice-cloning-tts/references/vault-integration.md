# Vault Integration with Hermes Agent

## Symlink Pattern

To make Obsidian vaults accessible to Hermes Agent:

```bash
# Create symlinks from Hermes profile to Obsidian vaults
ln -sf /home/hatem/Documents/Hafsa /home/hatem/.hermes/profiles/hafsa/vault-hafsa
ln -sf /home/hatem/Documents/Hatem\ Nad /home/hatem/.hermes/profiles/hafsa/vault-hatem-nad
```

## CLAUDE.md Router

Each vault should have a `CLAUDE.md` in its root that serves as a router for the AI agent. Key sections:
- **Instructions for AI** — how to navigate the vault
- **Index** — map of all subdirectories
- **Rules** — no deletion, add new files to index
- **User preferences** — persona-specific settings

## Dead Files vs Living Files

- **Dead files:** Not accessible to AI (on disconnected drives, random folders)
- **Living files:** Markdown files in a structured vault that AI can read/reference/use as context

## Obsidian + Hermes Architecture

```
User's Obsidian Vault (local)
    ↓ (symlink)
Hermes Profile/vault-name/
    ↓ (agent reads)
Context for AI responses, skills, memory, SOUL.md
```

## Benefits
- Visual graph view of AI's knowledge
- Edit AI skills/notes without touching code
- Sync across devices (Obsidian Sync or git)
- AI agent can reference specific files by path
