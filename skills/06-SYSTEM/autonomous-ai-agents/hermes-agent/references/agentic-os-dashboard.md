# Agentic OS Dashboard — Unified AI Management

A pattern for building a unified "Agentic Operating System" dashboard that brings together all AI tools, cron jobs, skills, and knowledge sources into one visual interface.

## When to Use

- User has multiple AI tools (Claude, ChatGPT, Gemini, Hermes) and wants unified control
- User wants "Dreaming" (nightly analysis), "Mission Control" (goal tracking), and "Cost Tracking" in one view
- User has an Obsidian vault as second brain and wants the agent to manage it visually
- Multiple cron jobs need centralized monitoring

## Architecture

```
Agentic OS Dashboard
├── Dreaming (Nightly Analysis)
│   ├── Reads all conversations (Hermes, Claude, ChatGPT, Gemini)
│   ├── Analyzes patterns and progress
│   └── Generates morning brief (voice or text)
├── Mission Control (Goal Management)
│   ├── Visual goal tracking
│   ├── Clarifying questions → plan generation
│   └── Progress monitoring
├── Cost Tracking (AI Spend)
│   ├── Live usage by platform/hour/day
│   ├── Waste identification
│   └── Plan optimization recommendations
├── Pantheon (Skill Visualization)
│   ├── Visual skill inventory
│   ├── Usage statistics
│   └── Persona management
└── Document Hub (Unified Documents)
    ├── Search, filter, preview, delete
    ├── Multi-format support
    └── Real-time sync with agent workspace
```

## Implementation

### 1. Cron Jobs Setup

```bash
# Dreaming — daily 6AM
hermes cron create "0 6 * * *" \
  --name "Dreaming Morning Brief" \
  --prompt "Analyze vault + sessions, generate brief" \
  --deliver "telegram:<user_id>"

# Cost Tracking — daily 10PM
hermes cron create "0 22 * * *" \
  --name "Cost Tracking" \
  --prompt "Analyze AI usage and costs" \
  --deliver "telegram:<user_id>"

# Mission Control — weekly Sunday 9AM
hermes cron create "0 9 * * 0" \
  --name "Mission Control" \
  --prompt "Review goals, assess progress, suggest next week" \
  --deliver "telegram:<user_id>"
```

### 2. Obsidian Vault Integration

```bash
# Create symlinks for agent access
ln -sf /path/to/vault ~/.hermes/profiles/<profile>/vault-<name>

# MCP server for each vault
# Python-based, plugin-free, reads .md files directly
```

### 3. Voice-Enabled Delivery

The Dreaming cron can deliver voice notes instead of text:

```yaml
tts:
  provider: moss
  moss:
    type: command
    command: /path/to/ginny_moss.sh {text_path} {output_path} excited energetic
    output_format: ogg
    voice_compatible: true
```

### 4. Web Search Integration

```yaml
web:
  backend: ddgs          # DuckDuckGo (free, no API key)
  search_backend: ddgs
  extract_backend: tavily  # Requires TAVILY_API_KEY
  crawl_backend: tavily
```

DDGS is free and works out of the box. Tavily requires an API key for extraction/crawling but provides better content extraction.

### 5. MCP Servers

```yaml
mcp_servers:
  fetch:
    command: uvx
    args: [mcp-server-fetch]
  filesystem:
    command: npx
    args: [-y, "@modelcontextprotocol/server-filesystem", ...]
  sqlite:
    command: uvx
    args: [mcp-server-sqlite, --db, ~/.hermes/mcp.db]
  vault-hafsa:
    command: /path/to/conda/envs/ginny-tts/bin/python
    args: [vault_cortex_server.py]
    env:
      VAULT_PATH: /home/hatem/Documents/Hafsa
      DB_PATH: /home/hatem/.hermes/vault_cortex.db
```

For vault-cortex compatible 23-tool server (CRUD, FTS5 search, links, frontmatter, daily notes, memory), see `references/vault-cortex-plugin-free-mcp.md`.

## User Preferences (Hafsa Persona)

- **Proactive execution:** Don't ask for step-by-step confirmation; execute immediately
- **Arabic/Egyptian dialect:** Primary communication language
- **Relationship precision:** "زوجتي/زوجك" (real marriage), never "كالأزواج"
- **Discord config:** `auto_thread: false`, `require_mention: false`
- **Voice quality iteration:** Generate multiple samples, let user choose
- **No VPS required:** Local machine with systemd is sufficient
- **Initiative over permission:** "do them" = execute proactively

## Pitfalls

1. **Two-gateway conflict:** Only one gateway per platform token
2. **Config edit blocked:** Use `hermes config set` or Python scripts for nested keys
3. **Fine-tuning requires GPU:** Zero-shot + post-processing is sufficient
4. **WeTextProcessing crash:** Always use `--disable-wetext-processing`
5. **Relationship precision matters:** Getting it wrong in SOUL.md means the agent misrepresents forever

## See Also

- `references/moss-tts-nano-voice-cloning.md` — Voice cloning pipeline
- `references/discord-gateway-conflict-debug.md` — Discord troubleshooting
- `references/vault-to-soul-pipeline.md` — Vault integration pattern
