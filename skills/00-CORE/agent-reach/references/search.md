# Search Tools

Exa AI search engine reference.

## Exa AI Search

High-quality AI search engine, strong for technical and code search.

```bash
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'
mcporter call 'exa.get_code_context_exa(query: "code question", tokensNum: 3000)'
```

### Use Cases

| Use Case | Args |
|-----|------|
| Web search | `web_search_exa(query: "...", numResults: 5)` |
| Code search | `get_code_context_exa(query: "...", tokensNum: 3000)` |

### Notes

- Strong on English content and technical docs
- Supports code-context search
- High-quality results

## Compare with Other Search Tools

| Tool | Source | Best For |
|-----|------|---------|
| Exa | agent-reach | English / technical / code search |
| Google | native | General web |
| GitHub Search | agent-reach (dev.md) | Repo / code search |
