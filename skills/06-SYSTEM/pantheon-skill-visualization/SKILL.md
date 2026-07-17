---
name: pantheon-skill-visualization
description: >
  MUST USE when user wants to view, manage, or visualize all agent skills and personas.
  Provides a unified visual overview of all installed skills, their usage statistics,
  and persona configurations.
  
  Key capabilities:
  - Visual skill inventory with usage stats
  - Persona management (create, edit, assign models)
  - Skill categorization and filtering
  - Model assignment per persona
  - Skill dependency mapping
  
  NOT for: creating new skills (use hermes-agent-skill-authoring), executing tasks.
metadata:
  hermes:
    tags: [pantheon, skills, visualization, personas, management]
    priority: high
---

# Pantheon — Skill & Persona Visualization

## Overview
Pantheon provides a visual representation of all agent skills and personas, making it easy to see what's available, what's being used, and how everything connects.

## Skill Categories

### 🤖 Autonomous AI Agents (4)
- claude-code, codex, hermes-agent, opencode

### 🎨 Creative (16)
- agent-reach, architecture-diagram, ascii-art, ascii-video, baoyu-infographic, claude-design, comfyui, design-md, excalidraw, humanizer, manim-video, p5js, popular-web-designs, sketch, songwriting-and-ai-music, voice-cloning-tts

### 🏥 Medical (3)
- ophthalmology-ai-retinal-analysis
- neurology-ai-brain-tumor-diagnosis
- internal-medicine-ai-diagnosis

### 📊 Data Science (1)
- jupyter-live-kernel

### 📧 Email (1)
- himalaya

### 🐙 GitHub (6)
- github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management, github-repo-discovery

### 🎬 Media (5)
- gif-search, heartmula, songsee, youtube-content, moss-tts-voice-cloning

### 🧠 MLOps (7)
- audiocraft-audio-generation, evaluating-llms-harness, huggingface-hub, llama-cpp, segment-anything-model, serving-llms-vllm, weights-and-biases

### 📝 Note Taking (1)
- obsidian

### 📈 Productivity (8)
- airtable, google-workspace, maps, nano-pdf, notion, ocr-and-documents, powerpoint, teams-meeting-pipeline

### 🔬 Research (5)
- arxiv, blogwatcher, llm-wiki, polymarket, research-paper-writing

### 🏠 Smart Home (1)
- openhue

### 📱 Social Media (1)
- xurl

### 💻 Software Development (12)
- github-repo-discovery, hermes-agent-skill-authoring, node-inspect-debugger, plan, python-debugpy, requesting-code-review, simplify-code, spike, systematic-debugging, test-driven-development

### 🔧 Agentic OS (1)
- agentic-os-dashboard

## Persona System

### Default Personas
| Persona | Model | Role | Use Case |
|---------|-------|------|----------|
| **Default** | openrouter/owl-alpha | General assistant | Everyday tasks |
| **Medical** | openrouter/owl-alpha | Medical specialist | Health questions, research |
| **Creative** | openrouter/owl-alpha | Creative assistant | Design, writing, art |
| **Technical** | openrouter/owl-alpha | Technical expert | Coding, DevOps, MLOps |
| **Research** | openrouter/owl-alpha | Research assistant | Academic research, papers |

### Persona Configuration
Each persona can have:
- Preferred model
- System prompt
- Skill subset
- Voice preset (for TTS)

## Usage

### View all skills
```bash
hermes -p hafsa skills list
```

### View skill details
```bash
skill_view(name="skill-name")
```

### Create new persona
1. Define persona name and role
2. Set preferred model
3. Configure system prompt
4. Assign skill subset
5. Set voice preset (optional)

## Visualization Format

### Skill Inventory Table
| Skill | Category | Priority | Status | Usage |
|-------|----------|----------|--------|-------|
| agent-reach | Creative | High | ✅ Active | High |
| ophthalmology-ai | Medical | High | ✅ Active | Medium |
| ... | ... | ... | ... | ... |

### Persona Assignment Table
| Persona | Model | Skills | Voice |
|---------|-------|--------|-------|
| Default | owl-alpha | All | caring |
| Medical | owl-alpha | Medical + Research | warm |
| Creative | owl-alpha | Creative + Media | energetic |
| Technical | owl-alpha | Dev + MLOps | crisp |
| Research | owl-alpha | Research + Arxiv | warm |
