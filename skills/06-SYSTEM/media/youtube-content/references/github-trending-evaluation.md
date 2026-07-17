# GitHub Trending Video Evaluation Pattern

When a YouTube video covers "GitHub Trending" for AI agents/tools, use this enhanced format:

## Output Structure for Trending Videos

### 1. Ranked Table
| # | Project | Description | Stars | Verdict |
|---|---|---|---|---|

### 2. Properties/Concepts by Category
Group findings into categories:
- **Core concepts** — the fundamental ideas
- **Problems identified** — what's broken
- **Solutions proposed** — how to fix it
- **Tools mentioned** — specific repos

### 3. Actionable Suggestions
Map to user's vault structure:
| Priority | Action | Target |
|---|---|---|
| High | Integrate immediately | `00-CORE/` or `01-PROJECTS/` |
| Medium | Evaluate when needed | `05-ARCHIVE/` or note |
| Low | Skip | — |

### 4. Ecosystem Mapping
Identify which layer each trending repo belongs to:
- Layer 1: Skills (capabilities)
- Layer 2: Memory (context)
- Layer 3: Perception (live data)
- Layer 4: Security (trust)

## Example (from 2026-06-24)
Video: "GitHub Trending — Top 10 this week"
- 5/10 repos were about "skills" (Layer 1)
- 1 was memory (Layer 2)
- 1 was perception (Layer 3)
- 1 was security (Layer 4)
- 2 were production tools (cross-layer)
