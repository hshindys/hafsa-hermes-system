# Vault-Cortex Compatible MCP Server (Plugin-Free)

When Docker is unavailable, build a Python MCP server that replicates vault-cortex's 23 tools.

## Why Plugin-Free?

The typical Obsidian + MCP setup requires: Obsidian app → Local REST API plugin → MCP server wrapping the REST API. This means Obsidian must stay open, the plugin breaks on updates, and TLS/SSL issues with self-signed certs.

Plugin-free approach: read `.md` files directly from disk via fastmcp SDK.

## Implementation

```python
from fastmcp import FastMCP
import os, json, re, sqlite3

mcp = FastMCP("vault-cortex")
VAULT_PATH = os.environ.get("VAULT_PATH")
DB_PATH = os.environ.get("DB_PATH", "/home/hatem/.hermes/vault_cortex.db")

# FTS5 for full-text search
def get_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(path, content)")
    return db

def index_vault():
    """Index all .md files for FTS5 search."""
    db = get_db()
    db.execute("DELETE FROM notes_fts")
    for root, dirs, files in os.walk(VAULT_PATH):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith(".md"):
                fp = os.path.join(root, f)
                rp = os.path.relpath(fp, VAULT_PATH)
                with open(fp, 'r') as fh:
                    db.execute("INSERT INTO notes_fts VALUES (?, ?)", (rp, fh.read()))
    db.commit(); db.close()
```

## 23 Tools (vault-cortex compatible)

| Category | Tools |
|----------|-------|
| CRUD | read_note, write_note, patch_note, replace_in_note, list_notes, delete_note |
| Search | search (FTS5), search_by_tag, search_by_folder, recent_notes, list_tags |
| Memory | get_memory, update_memory, delete_memory, list_memory_files |
| Properties | list_property_keys, list_property_values, search_by_property, update_properties |
| Links | get_backlinks, get_outgoing_links, find_orphans |
| Daily | get_daily_note |
| Stats | get_vault_stats |

## Hermes Config

```yaml
mcp_servers:
  vault-hafsa:
    command: /path/to/conda/envs/ginny-tts/bin/python
    args: ["/home/hatem/.hermes/scripts/vault_cortex_server.py"]
    env:
      VAULT_PATH: "/home/hatem/Documents/Hafsa"
      DB_PATH: "/home/hatem/.hermes/vault_cortex.db"
```

## Pitfalls

1. **fastmcp must be installed in the same Python env as the MCP server script**
2. **FTS5 search uses `snippet()` for context highlighting** — requires `tokenize='porter'`
3. **Backlinks use wikilink pattern matching**: `[[target]]` or `[[target|text]]`
4. **Frontmatter parsing**: check for `---` delimiters, parse YAML manually (no PyYAML dependency needed for simple keys)
5. **Delete moves to `.trash/`** instead of permanent deletion (Obsidian-compatible)
6. **Index on startup** for fast subsequent searches; re-index after write operations
