---
name: medical-research-synthesis
description: >
  MUST USE when user wants to research medical topics, summarize academic papers,
  or create medical domain skills from research. Covers: vault search for existing
  research, internet search for latest studies (via Exa), paper summarization,
  priority ranking, and skill generation from findings.
  
  Key capabilities:
  - Search local vault for existing medical research
  - Search internet (Exa) for latest academic studies
  - Summarize papers with key findings and clinical relevance
  - Rank by priority (High/Medium/Low)
  - Generate domain-specific skills from research
  - Create plugin for medical knowledge base
  
  NOT for: patient diagnosis, treatment recommendations, drug prescriptions.
metadata:
  hermes:
    tags: [medical-research, literature-review, skill-generation, synthesis]
    priority: high
---

# Medical Research Synthesis

## Overview
Search both local vault and internet for medical research, synthesize findings, and generate actionable skills and knowledge bases.

## When to use
- User asks to research a medical topic
- User wants latest academic studies in a field
- User wants to create medical skills from research
- User mentions "ابحث", "research", "latest studies", "papers"

## Workflow

### Step 1: Vault Search
Search the Obsidian vault for existing research files:
```bash
# Search for medical files
find ~/Documents/Hafsa-1/ -name "*.md" | xargs grep -l "medical\|طب\|ophthalmology\|neurology\|internal medicine"

# Search specific subdirectories
ls ~/Documents/Hafsa-1/AI-Skills-Research/
ls ~/Documents/Hafsa-1/🏥 Medical/
```

### Step 2: Internet Search
Use Exa search (via mcporter) for latest academic research:
```bash
mcporter call 'exa.web_search_exa(query: "ophthalmology AI 2025 2026 breakthroughs", numResults: 5)'
mcporter call 'exa.web_search_exa(query: "neurology deep learning diagnosis 2025 2026", numResults: 5)'
mcporter call 'exa.web_search_exa(query: "internal medicine AI agent 2025 2026", numResults: 5)'
```

**Note:** web_search and web_extract may fail if Firecrawl API key is not configured. Use mcporter/Exa as fallback.

### Step 3: Summarize Each Paper
For each paper found:
1. Title, source, date
2. Core concept (2-3 sentences)
3. Key results (metrics, accuracy)
4. Clinical relevance (how it helps patients)
5. Priority ranking

### Step 4: Priority Ranking
| Priority | Criteria |
|----------|----------|
| 🔴 High | Directly applicable to user's medical fields (ophthalmology, neurology, internal medicine), recent (2025-2026), high-impact journal |
| 🟠 Medium | Related field, good methodology, useful for background |
| 🟡 Low | Older, tangential, or low-impact |

### Step 5: Create Skills
For each priority tier, create a skill with:
- SKILL.md with full research summary
- references/ for detailed paper notes
- scripts/ for any reproducible analysis

### Step 6: Create Plugin
Build a knowledge base plugin that:
- Indexes all medical research
- Provides search and filter
- Maps conditions to AI models
- Tracks research updates

## User Preferences (Hafsa Persona)
- **Proactive:** Don't wait for step-by-step instructions. When user says "ابحث في الأبحاث الطبية", immediately search vault + internet, summarize, rank, and create skills.
- **Arabic-first:** Summaries in Arabic (Egyptian dialect), technical terms in English
- **Tables over prose:** Use tables for comparisons, bullet points for lists
- **Action-oriented:** Always end with concrete next steps and artifacts (skills, files)
- **Medical fields:** Ophthalmology 👁, Neurology 🧠, Internal Medicine 🏥

## Pitfalls
- **web_search fails:** Use `mcporter call 'exa.web_search_exa(...)'` instead
- **PubMed blocked:** Use Jina Reader with PubMed URL (`r.jina.ai/https://pubmed.ncbi.nlm.nih.gov/...`), or search arXiv via direct API
- **Google blocked:** Use Exa or DuckDuckGo via Jina Reader
- **Rate limiting:** Space out searches, use `--skip-download` for yt-dlp
- **arXiv returns XML:** Parse with Python `xml.etree.ElementTree`, not raw text
- **Paywalled papers:** Extract abstract only, note "full text requires access"
- **MOSS-TTS import error:** Use subprocess to `infer.py`, never `from moss_tts_nano import MOSS_TTS_Nano`

## Example Output Structure
```
📋 Medical Research Summary
├── 🔴 Priority 1: [High-impact paper]
│   ├── Summary
│   ├── Clinical relevance
│   └── Action items
├── 🟠 Priority 2: [Medium-impact paper]
└── 🟡 Priority 3: [Background paper]

🔧 Skills Created:
├── [skill-name-1]
└── [skill-name-2]
```
