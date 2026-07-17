---
name: memory-search
description: Search past Hermes sessions and memory files relevant to the current task
---

# Memory & Session Search Protocol

When asked to recall prior work, check memory and session history in this order:

1. **Memory store**: read memory for durable facts / user prefs
2. **Session history**: session_search with a focused query
3. **Vault / notes**: read any known daily or project note if relevant
4. **If nothing found**: report that clearly instead of guessing