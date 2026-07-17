---
name: github-trending-skill-scout
description: "Monitor GitHub trending for new AI agent skills, evaluate them for your vault, and integrate useful ones. Covers: finding trending repos, filtering for skill/agent relevance, security scanning, and structured audit/trust decisions."
triggers:
  - "github trending skills"
  - "trending agent skills"
  - "new skills from github"
  - "skill scout"
  - "find new agent skills"
  - "github trending repos"
  - "skills audit"
  - "evaluate new skill"
---

# GitHub Trending Skill Scout

## When to use
- User shares a GitHub trending video/list and wants to know what's useful
- You want to proactively scan for new high-quality agent skills
- User asks "what's trending on GitHub this week for AI agents?"
- You find a repo in a video description and want to evaluate it

## The Workflow

### 1. Observe — Find Trending Repos
Sources:
- YouTube videos titled "GitHub Trending" or "Top 10 GitHub repos this week"
- GitHub Trending page: `https://github.com/trending`
- Video transcripts (use youtube-content skill to extract)

### 2. Orient — Filter for Your Needs
Ask: Does this repo solve a problem I actually have?

**Relevance filters:**
- Does it fill a gap in my current skill library?
- Is it production-ready (has issues, forks, discussions) or just hype?
- Does the author have credibility (known educator, engineer at major company)?
- Is the license compatible (MIT/Apache for tools)?

**Red flags (skip if present):**
- 0 issues, 0 forks, but 10k+ stars in 3 weeks = likely star inflation
- No commits in last 6 months
- Author is anonymous or newly created
- Description is vague buzzwords with no concrete use case

### 3. Decide — Audit Before Install
Before adding any skill to your vault:
1. Read the SKILL.md fully
2. Run `skill-specter` if available (NVIDIA garak-based scanner)
3. Check for: prompt injection vectors, data exfiltration paths, unnecessary permission requests
4. If it passes, clone to appropriate OODA skill folder

### 4. Act — Integrate or Archive
- **Integrate:** Copy skill to `~/.hermes/skills/00-CORE/` or appropriate category
- **Document:** Add entry to Skills-Audit file with date, verdict, and reason
- **Skip:** If not useful now, note it in case needs change later

## Skills Ecosystem Pattern (from 2026-06-24)

A healthy skills ecosystem forms in layers around a trend:

```
Layer 1: Skills (the capabilities themselves)
  → Matt Pocock Skills, Addy Osmani Agent Skills

Layer 2: Memory (context for skills)
  → Codebase Memory MCP, Vector indexes

Layer 3: Perception (live data for skills)
  → Agent Reach (internet access), RAG pipelines

Layer 4: Security (trust & safety for skills)
  → Skill Specter (Nvidia), Security scanners
```

When evaluating a trending repo, ask which layer it belongs to and whether that layer is already covered.

## Output Format

For each trending repo, produce:

| # | Repo | Category | Stars | Verdict | Action |
|---|---|---|---|---|---|
| 1 | owner/repo | skill/tool/mcp/model | +Xk | Keep/Skip/Scan first | Integrate/Skip/Archive |

**Verdict criteria:**
- **Keep:** Fills a gap, credible author, active development
- **Scan first:** Useful but needs security review
- **Skip:** Red flags, duplicate of existing skill, or irrelevant

## Pitfalls

### Star inflation detection
```
Stars gained in 1 week > 10,000 + 0 issues + 0 forks = SUSPICICIOUS
Real projects have community engagement (issues, PRs, discussions)
```

### Video creator bias
YouTube tech reviewers often promote repos they're affiliated with. Cross-check:
- Is the repo actually #1 on GitHub trending that week?
- Does the creator disclose any sponsorship?

### Install-before-evaluate trap
Never install a skill before reading its SKILL.md. Some trending repos:
- Require API keys you don't have
- Need specific hardware (GPU, etc.)
- Have dependencies that conflict with your setup

## References
- `references/skill-audit-template.md` — Template for documenting skill evaluations
- `references/ecosystem-layers.md` — Detailed explanation of the 4-layer skills ecosystem
