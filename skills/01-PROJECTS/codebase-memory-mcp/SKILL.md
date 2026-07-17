---
name: codebase-memory-mcp
description: "MCP server that gives your AI agent persistent memory of your entire codebase. Indexes all files once so Claude Code / Cursor / any MCP-compatible agent can recall project structure instead of re-reading from scratch each turn. Written in C for speed."
triggers:
  - "codebase memory"
  - "project memory"
  - "MCP memory"
  - "codebase index"
  - "file index"
---

# Codebase Memory MCP

## What it does
High-performance MCP server that indexes your entire project codebase. Tools like Claude Code can recall how the project fits together instead of starting from scratch each turn.

## Why it matters
When your AI agent works on a big project, it wastes huge amounts of time and money re-reading the same files over and over. This gives it a fast, persistent memory.

## How to use
1. Install the MCP server (check GitHub repo for latest)
2. Add to your MCP client config:
   ```json
   {
     "mcpServers": {
       "codebase-memory": {
         "command": "codebase-memory",
         "args": ["--project-root", "/path/to/project"]
       }
     }
   }
   ```
3. Your agent will now have context of your full project structure

## Features
- Written in C for speed
- Indexes everything once
- Plugs into any MCP-compatible editor
- Works with Claude Code, Cursor, etc.
- Persistent across sessions

## Source
GitHub Trending #3 — week of 2026-06-24
