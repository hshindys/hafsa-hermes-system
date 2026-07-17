# Skills Ecosystem Layers

When evaluating trending repos, map them to layers. A healthy vault has all 4.

## Layer 1: Skills (Capabilities)
The actual tools your agent uses. Examples:
- `medical-research` — search and summarize papers
- `novel-writing` — fiction writing rules
- `agent-reach` — internet access

**Question to ask:** "Does this give my agent a new capability it doesn't have?"

## Layer 2: Memory (Context)
Skills need context to be effective. This layer provides:
- Codebase structure memory
- User preferences and history
- Project-specific knowledge

**Question to ask:** "Does this help my agent remember things across sessions?"

## Layer 3: Perception (Live Data)
Skills that give your agent access to real-time information:
- Web browsing
- API access
- RSS feeds
- Live pricing, scores, news

**Question to ask:** "Does this give my agent access to information it couldn't get otherwise?"

## Layer 4: Security (Trust)
As skills multiply, security becomes critical:
- Skill scanning before install
- Permission validation
- Prompt injection detection

**Question to ask:** "Does this make my agent safer?"

## The Ecosystem Pattern (observed 2026-06-24)

When GitHub trended "skills" for AI agents, the top 10 repos mapped to all 4 layers:

| Layer | Repo | Role |
|---|---|---|
| 1 (Skills) | Matt Pocock Skills | Production-grade skill set |
| 1 (Skills) | Addy Osmani Agent Skills | Curated skill library |
| 2 (Memory) | Codebase Memory MCP | Project structure memory |
| 3 (Perception) | Agent Reach | Live internet access |
| 4 (Security) | Skill Specter (Nvidia) | Skill security scanner |

**Key insight:** Trends often produce complementary repos across all layers simultaneously. Evaluate the ecosystem, not just individual repos.
