---
name: medical-research-skill-pipeline
description: "Use when user wants to research medical topics and create domain-specific skills from findings. Covers: Exa/PubMed search → summarization → skill creation → plugin generation. For ophthalmology, neurology, internal medicine, and clinical research."
version: 1.0.0
author: Hafsa Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [medical-research, skill-creation, ophthalmology, neurology, clinical]
    related_skills: [research-paper-writing, hermes-agent-skill-authoring]
---

# Medical Research → Skill Pipeline

## Overview
Search for latest medical research, summarize findings, and create deployable skills and plugins. This pipeline bridges the gap between academic research and agent capabilities.

## Workflow

### 1. Search
```bash
# Use Exa search (via mcporter) for latest research
mcporter call 'exa.web_search_exa(query: "ophthalmology AI 2025 2026 breakthroughs", numResults: 5)'

# Or use Jina Reader for specific URLs
curl -s "https://r.jina.ai/https://pubmed.ncbi.nlm.nih.gov/search/?q=query"
```

### 2. Summarize
For each paper/research found:
- Title, source, date
- Core concept (2-3 sentences)
- Key results (metrics, accuracy)
- Clinical applications
- Priority level (High/Medium/Low)

### 3. Create Skill
Use `skill_manage(action='create')` with:
- Class-level name (not session-specific)
- Trigger-focused description
- Structured SKILL.md with overview, usage, pitfalls
- `references/` for detailed research notes

### 4. Create Plugin (when applicable)
For searchable/reference tools:
- Python script in `plugins/<name>/`
- Register in Hermes config if needed

## Priority Classification

| Priority | Criteria |
|----------|----------|
| 🔴 High | Directly relevant to user's health profile or stated goals |
| 🟠 Medium | General medical knowledge, useful for conversations |
| 🟡 Low | Background reference, nice-to-have |

## User-Specific Rules

**CRITICAL for this user:**
1. **No seafood suggestions** — severe allergy (user: Hatem)
2. **No direct medical advice** — all output is reference/analysis only
3. **Always recommend consulting healthcare professional**
4. **Medication reminders** — include timing and dosage in health-related outputs
5. **Arabic (Egyptian dialect)** — primary language for user communication

## Research Domains (User-Specific)

| Domain | Focus Areas | User Relevance |
|--------|-------------|----------------|
| Ophthalmology | Retinal imaging, AI detection, surgical video | User's specialty |
| Neurology | Brain tumor classification, MRI AI | User's specialty |
| Internal Medicine | Clinical diagnosis, LLM agents | User's specialty |
| Voice Cloning | MOSS-TTS-Nano, persona voice | Active project |
| Agentic OS | Dreaming, mission control, cost tracking | Active project |

## Output Template

```markdown
# 🏥 Medical Research Summary
> Last updated: YYYY-MM-DD

## 🔴 Priority 1 — [Domain]
### [Paper Title]
- **Source:** [Journal, Year]
- **Key Results:** [metrics]
- **Application:** [clinical use]

## Skills Created
| Skill | Domain | Priority |
|-------|--------|----------|
| skill-name | domain | 🔴 High |
```

## Verification Checklist

- [ ] Searched at least 2 sources (Exa + PubMed/Jina)
- [ ] Summarized each finding with source attribution
- [ ] Classified by priority
- [ ] Skills created with proper frontmatter
- [ ] No medical advice (documentation only)
- [ ] No seafood mentions anywhere
- [ ] Medication reminders included where relevant
