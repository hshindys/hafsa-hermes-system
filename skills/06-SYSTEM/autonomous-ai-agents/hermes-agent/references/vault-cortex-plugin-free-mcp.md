# Vault-Cortex Compatible MCP Server (Plugin-Free)

A Python MCP server that provides 23 tools matching vault-cortex functionality — reads `.md` files directly from disk with no Obsidian plugin, no HTTP server, no Obsidian app running.

## When to Use

- User has a large Obsidian vault (thousands of notes, hundreds of folders)
- User wants full CRUD + search + links + frontmatter + daily notes access
- User wants FTS5 (SQLite full-text search) with BM25 scoring
- User wants the agent to manage vault files programmatically
- Docker is not available (shared machine, no root access)

## Architecture

```
Agent → MCP Client → vault_cortex_server.py → SQLite FTS5 + filesystem
```

## Implementation

Location: `~/.hermes/scripts/vault_cortex_server.py`

### Dependencies

```bash
# In any Python env with fastmcp
pip install fastmcp
```

### Server Setup

```python
from fastmcp import FastMCP
import os, json, re, sqlite3

mcp = FastMCP("vault-cortex")
VAULT_PATH = os.environ.get("VAULT_PATH", "/path/to/vault")
DB_PATH = os.environ.get("DB_PATH", "/path/to/vault_cortex.db")

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(path, content, tokenize='porter')")
    db.execute("CREATE TABLE IF NOT EXISTS vault_meta (key TEXT PRIMARY KEY, value TEXT)")
    db.commit()
    return db

def index_vault():
    """Index all .md files for full-text search."""
    db = get_db()
    db.execute("DELETE FROM notes_fts")
    for root, dirs, files in os.walk(VAULT_PATH):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, VAULT_PATH)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    db.execute("INSERT INTO notes_fts (path, content) VALUES (?, ?)", (rel_path, content))
                except:
                    continue
    db.commit()
    db.close()
```

### 23 Tools Available

| Category | Tools |
|----------|-------|
| **CRUD** | `read_note`, `write_note`, `patch_note`, `replace_in_note`, `list_notes`, `delete_note` |
| **Search** | `search` (FTS5 BM25), `search_by_tag`, `search_by_folder`, `recent_notes`, `list_tags` |
| **Memory** | `get_memory`, `update_memory`, `delete_memory`, `list_memory_files` |
| **Properties** | `list_property_keys`, `list_property_values`, `search_by_property`, `update_properties` |
| **Links** | `get_backlinks`, `get_outgoing_links`, `find_orphans` |
| **Daily** | `get_daily_note` |
| **Stats** | `get_vault_stats` |

### Hermes Config

```yaml
mcp_servers:
  vault-hafsa:
    command: /path/to/conda/envs/ginny-tts/bin/python
    args: [/path/to/vault_cortex_server.py]
    env:
      VAULT_PATH: /home/hatem/Documents/Hafsa
      DB_PATH: /home/hatem/.hermes/vault_cortex.db
  vault-hatem:
    command: /path/to/conda/envs/ginny-tts/bin/python
    args: [/path/to/vault_cortex_server.py]
    env:
      VAULT_PATH: /home/hatem/Documents/Hatem Nad
      DB_PATH: /home/hatem/.hermes/vault_cortex_hatem.db
```

### Indexing on Startup

The server automatically indexes the vault on startup. For large vaults (3000+ notes), this takes 5-15 seconds. Call `index_vault()` after any batch write operations.

### Performance

| Vault Size | Notes | Index Time | Search |
|------------|-------|------------|--------|
| Small | ~100 | <1s | <100ms |
| Medium | ~500 | 2-3s | <200ms |
| Large | ~3000 | 10-15s | <500ms |

## Pitfalls

### FTS5 Special Characters
FTS5 treats certain characters as operators (`-`, `*`, `+`). Escape user queries or wrap in quotes to avoid syntax errors.

### Concurrent Writes
SQLite handles concurrent reads fine but concurrent writes can lock. For batch operations, index once at the end rather than after each file.

### Frontmatter Parsing
Simple YAML frontmatter parser — doesn't handle multi-line values or complex nested structures. For complex frontmatter, use a proper YAML library.

### Delete Safety
`delete_note` moves to `.trash/` folder rather than permanent deletion. This is intentional — the agent should never permanently delete user data without explicit confirmation.

### Memory Layer
The `vault_meta` table stores key-value pairs (agent memories). Use for persistent state that survives across sessions but is specific to the vault.

## Comparison with Other Options

| Feature | This Server | vault-cortex (Docker) | ObsidianMCPServer |
|---------|-------------|----------------------|-------------------|
| Language | Python | TypeScript/Docker | Swift |
| Setup | pip install | Docker compose | Build from source |
| Tools | 23 | 23 | ~10 |
| Search | FTS5 BM25 | FTS5 BM25 | Basic |
| Write | ✅ | ✅ | ❌ |
| Links | ✅ | ✅ | ✅ |
| Frontmatter | ✅ | ✅ | ✅ |
| Daily notes | ✅ | ✅ | ❌ |
| Auth | None | OAuth 2.1 | None |
| Docker | Not required | Required | Not required |

## User Preference: Multiple Vaults

User has two vaults (Hafsa + Hatem Nad). Configure separate MCP server instances for each with different `VAULT_PATH` and `DB_PATH`. The agent should always check BOTH vaults when searching for information.

## GLM-5.2 for Design Tasks

When the user wants to build UI/UX, landing pages, or dashboards, GLM-5.2 (via OpenRouter) is available and excellent for long-context design tasks. It maintains design consistency (colors, typography, spacing) across multi-page outputs.

- Model ID: `z-ai/glm-5.2`
- Provider: openrouter
- Context: 1M tokens, 128K output
- Supports: tool calling, structured output, deep thinking
- Best for: Complex design systems, multi-page consistent UI, landing pages

Cheaper alternative: `z-ai/glm-5.1` (202K context) for simpler tasks.

### Hermes Config for GLM-5.2
```yaml
models:
  glm-5.2:
    id: z-ai/glm-5.2
    provider: openrouter
    context_length: 1048576
    supports_tool_calling: true
    supports_thinking: true
    best_for: [coding, design, long-context, ui-building]
```

Switch to it with `/model z-ai/glm-5.2` for design-heavy tasks, then switch back to default when done.
