---
name: agentic-os-dashboard
description: >
  MUST USE when building or managing an agentic operating system dashboard.
  Covers: Dreaming (nightly analysis), Mission Control (goal management),
  Cost Tracking (AI spend monitoring), Pantheon (skill visualization),
  Document Hub (unified document management).
  
  Key capabilities:
  - Visual intelligence layer for Hermes agent
  - Unified view of all AI tools and conversations
  - Goal tracking with clarifying questions
  - Cost breakdown by platform/hour/day
  - Skill and persona management
  - Document creation, search, filter, and deletion
  
  NOT for: basic chat, simple task execution, single-tool usage.
metadata:
  hermes:
    tags: [agentic-os, dashboard, visual-intelligence, unified-ai]
    priority: high
---

# Agentic OS Dashboard

## Core Concept
Unify all AI tools into one visual intelligence layer. Solve context isolation by bringing everything together.

## Key Features

### 1. Dreaming (Nightly Analysis)
- Agent thinks about everything you've done overnight
- Reads all conversations (Hermes, Claude, ChatGPT, Gemini)
- Generates daily morning brief with improvement suggestions
- Compounds progress without willpower

### 2. Mission Control (Goal Management)
- Visual dashboard for goals and progress
- Agent asks clarifying questions to build detailed plans
- Mid-term goals (weeks to months)
- Dynamic insights by connecting data sources

### 3. Cost Tracking (AI Spend Monitoring)
- Live usage by hour/day for each AI platform
- Identify waste and optimize plans
- Context window remaining alerts
- Downgrade/upgrade recommendations

## Cost Tracking Daily Report Pattern

### Objective
Run a lightweight daily cost/usage report and deliver a short Telegram-style summary.

### Verified behavior and fail-soft handling
- OpenRouter usage endpoint: `/api/v1/auth/key`
  - Common case: returns `data.credit_limit`, `data.usage`, `data.is_free_tier`
  - Fallback case: returns an `error` object. Report `credits_remaining: N/A`, `usage_today: N/A`, `is_free_tier: N/A`
- `hermes cron list` may report `0` jobs even when jobs are configured; treat as a signal, not definitive health verdict.
- Session counts should be computed from dated session filenames in the profile sessions directory.
- Use instance-level `.usage.json` only for skill-level usage trends; it does not provide monetary cost.

### Report sections
- Daily AI/cost snapshot
- Disk usage for profile, sessions, skills
- Top skills used today with use_count
- Suggestions to save money / reduce waste
- OpenRouter health check result

### Output rules
- Short, scannable, Arabic-friendly
- Always include clear numeric fields
- Include at least 3 actionable suggestions even on “no event” days

### 4. Pantheon (Skill Visualization)
- Visual overview of all skills and personas
- Each persona can have its own model
- Easy skill editing without code
- Skill usage statistics

### 5. Document Hub (Unified Document Management)
- Single location for all agent-created documents
- Search, filter, preview, delete
- Support for multiple formats (text, HTML, markdown, code)
- Real-time sync with agent workspace

## Implementation Guide

### Step 1: Set up Dreaming cron job
```
Schedule: Daily at 6:00 AM
Prompt: Analyze all conversations from the past 24 hours, identify patterns, suggest improvements, remind about medications
Delivery: Telegram voice note
```

### Step 2: Set up Mission Control cron job
```
Schedule: Weekly on Sunday at 9:00 AM
Prompt: Review goals, assess progress, suggest next week's plan
Delivery: Telegram text
```

### Step 3: Set up Cost Tracking cron job
```
Schedule: Daily at 10:00 PM
Prompt: Analyze AI usage and costs, identify waste, suggest optimizations
Delivery: Telegram text
```

### Step 4: Create Document Hub
- Use Obsidian vault as document backend
- Create symlinks for agent workspace
- Set up search and filter capabilities
- Enable real-time sync

## Usage Guidelines
1. Always confirm understanding before building
2. Ask clarifying questions
3. Provide visual previews when possible
4. Follow existing design patterns
5. Enable live updates for all changes

## User Preference: Proactive Execution
User prefers the agent to act without asking for confirmation on every step.
When user says "ابدأ بالتنفيذ" or "اعمل اللي انتى عاوزة تعمليه", execute
immediately without further questions.

## Skill Library Update
This session produced a durable lesson for the cost-tracking workflow: handle OpenRouter error responses and cron list return-0 gracefully, and surface numeric summary fields in Telegram-style reports. That pattern is now encoded above and should be reused by future cost-tracking jobs.