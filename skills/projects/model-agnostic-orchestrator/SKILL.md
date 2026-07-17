---
name: model-agnostic-orchestrator
description: >
  MUST USE when assigning the right model to the right task and orchestrating
  multiple agents/projects in parallel. Encodes cost-aware model routing,
  per-skill model mapping, nightly dreaming, and project-level orchestration
  patterns for Hermes Agent. Applies the "Level 3-7" workflow from the 
  seven-level Hermes mastery framework.
metadata:
  hermes:
    tags: [model-routing, orchestration, multi-agent, cost-aware, async]
    priority: high
---

# Model-Agnostic Orchestrator

## When to use
Use when:
- The user says “do it”, “build the orchestrator”, “model routing”, “assign model per skill/task”
- Building or updating the agentic dashboard / Dreaming / Mission Control
- Running multiple projects/agents in parallel
- Reducing AI spend by avoiding expensive models for simple tasks
- Setting up nightly analysis, weekly briefs, or scheduled deliverables

## Standing rules
1. Cost first: prefer cheaper/free models for simple tasks.
2. Persona defaults: medical/legal/safety-critical → strong model; creative/research → capable but cheaper if adequate.
3. Never auto-run heavy orchestration from a cron job unless explicitly configured.
4. Dreaming/Nightly analysis must be explicit, scannable, Arabic-friendly, and safe-to-skip when nothing changed.

---

## 1. Model Routing Rules

### Default tiers
| Tier | Use case | Preferred models |
|---|---|---|
| S | Heavy reasoning, long-horizon build, medical reasoning, orchestration | Opus-class / GPT-5-class / best available |
| A | Research synthesis, complex drafting, coding, review | Sonnet-class / GPT-4.1-class |
| B | Simple QA, formatting, translation, Telegram/Discord replies | Flash-class / DeepSeek V4 Flash / free OpenRouter |
| C | Summaries, reminders, low-stakes automation | Free / lightweight |

### Routing guidelines
- Start cheap. Step up only when the task fails or quality drops.
- Do not pin a single global model for all skills/tasks.
- For medical-only flows, prefer strong model + medical skills, no shortcuts.
- For novel writing, prefer capable creative model; gateway must preserve Arabic RTL.

### Per-project routing hints
| Project | Recommended tier | Notes |
|---|---|---|
| Novel (كرون) | A or S for drafting | Arabic-only, creative |
| World Cup 2026 | B | Fixtures/results lookup |
| Al-Ahly tracker | B | Match summaries |
| Medical reminders | A | Safety — concise Arabic reply |
| Lola / Dina | S or A depending on task | Multi-agent / coding |
| Daily briefings | B | Short, scannable |

---

## 2. Persona / Skill Model Mapping

Each project can have its own effective persona with preferred model tier.
Use persona-system to encode this; this skill defines the routing logic.

Example mapping:
- Hafsa default → Tier B “owl-alpha” for chat + reminders.
- Hafsa medical → Tier A for medical skills only.
- Hafsa builder → Tier S for coding/build workflows.

Rule: never assign Tier S to a never-stop cron; it burns credits and often over-thinks simple output.

---

## 3. Orchestrator Pattern

### Concept
One Hermes instance acts as orchestrator; child agents run as delegated workers.
Orchestrator only coordinates, summarizes, and routes. It does not do all the work itself.

### Topology for Hatem’s setup
```
Orchestrator (Hafsa daily context)
├── لولا — project brain / notes
├── دينا — office/assistant workspace
├── World Cup 2026 — fixtures/rankings
├── Al-Ahly tracker — match follow-up
├── Novel كرون — chapter + character workflow
└── Medical reminders — morning/evening safe pings
```

### When to spawn children
- Long research tasks
- Sports/Web lookup with structured output
- Novel chapter drafting + character consistency check
- World Cup bracket updates
- Vault maintenance that can be noisy

### When NOT to spawn
- One-shot reminders
- Simple questions
- Anything under 2 tool calls

---

## 4. Dreaming / Nightly Analysis

### Purpose
Compounds progress overnight without willpower. Reads recent vault + project changes,
produces a short Arabic morning brief with improvement suggestions.

### Job spec
- Schedule: daily 23:00 Cairo
- Deliver: Telegram home channel
- Output: short Arabic brief, ≤12 lines
- Silence rule: if no meaningful changes, send “مافيش تغيير يستاهل الليلة”
- Never touch novel chapters without explicit request
- Prefer MCP vault APIs: recent_notes, find_orphans, vault stats

### Brief format
```
🌙 حفصة — Vision الليلة
- التعديلات: N ملف
- المشاريع النشطة: ...
- فكرة/ملاحظة: ...
- بكرة؟: ⚡ ...
```

---

## 5. Weekly Brief Pattern (Slack/Discord/Telegram)

- Sunday 09:00 Cairo
- Scope: Al-Ahly, World Cup, Novel progress, Medical follow-ups
- Format: 6-10 bullets, Arabic RTL, priorities marked

---

## 6. Cost Control

- Track OpenRouter credits weekly via status/cost checks.
- Kill runaway loops before they finish a session.
- If a job repeats empty success, pause it.
- Prefer free/cheap models for cron-safe automations.

---

## 7. Crew / Sub-Agent Prompt Templates

Use these when spawning child agents via delegate_task:

### Research agent
```
Goal: deep research on <topic>.
Constraints: return structured Arabic summary + priority table.
Tools: web, terminal, file.
```

### Builder agent
```
Goal: build/iterate on <project> artifact.
Constraints: produce real files under <absolute path>, verify output exists.
Tools: terminal, file, code execution.
```
## 8. Anti-patterns

- Do not give Hermes every MCP connection “just because”.
- Do not use heavy models for Telegram status pings.
- Do not run knowledge-crunching cron jobs at high frequency; nightly/weekly is enough.
- Do not trust a single cron-list response as health truth; verify via manual probe.

## 9. Cron Model Override Pitfall

`cronjob action=update` with `model=` does **not** reliably persist model/provider changes.
The job may still report the previous model in `cronjob list`.

Fix path:
1. Edit the profile-local `cron/jobs.json` directly via `patch` / `write_file`.
2. Restore the `model`, `provider`, and `base_url` fields on the target job object.
3. Confirm with `cronjob action=list` and re-read the job.

## 10. Tool Adoption / Missing-Repo Rule

When the user asks to install a trending tool and `gh search repos` returns no matching repo:
- Do not invent install steps.
- Record the missing-source status in `/home/hatem/Documents/Hafsa/01-Projects/Tools/status.md`.
- Ask the user for exact source/repo/URL before retrying.

## 12. Durable Sessions, Verifier, and Agent Manifest

Use this pattern when building robust cron-driven automations so jobs resume after failure and the agent can validate its own output.

### Durable session hook
- Script: `/home/hatem/.hermes/profiles/hafsa/scripts/durable-session-hook.sh`
- Command pattern inside cron prompt:
  - Resume: `bash .../durable-session-hook.sh <job_id> resume`
  - Checkpoint: `bash .../durable-session-hook.sh <job_id> checkpoint "note"`
- Each cron run reads the last checkpoint, acts from that state, then writes a new checkpoint on completion.

### Verifier script
- Script: `/home/hatem/.hermes/profiles/hafsa/scripts/project-verifier.sh`
- Usage: `project-verifier.sh <job_id> [require_checkpoint=1]`
- Exit codes: `VERIFIER=PASS|FAIL` plus metadata. Cron pipelines should stop and report on FAIL.

### Per-project binding
- Every production project should carry:
  - `SPEC.md` — Spec side of Karpathy method
  - `agent-manifest.json` — Skills/channels/MCP/schedule/cron_job_id
  - `lessons.md` or `OUTPUT/lessons.md` — KB side of Karpathy method
- Mapping to Karpathy method:
  - Spec → `SPEC.md` / existing `MASTER-PROMPT.md`
  - Verifier → `project-verifier.sh` + HITL approval gate for sensitive ops
  - Knowledge Base → `lessons.md` + vault/MCP stores

### Human-in-the-loop approval gate
For any sensitive operation (transfer, withdraw, payment, send to external account):
1. Stop before execution.
2. Emit `[PENDING APPROVAL: <action summary>]` and await explicit approval.
3. Only execute after approval token matches the pending action.

### Manifest-driven deployment
- `agent-manifest.json` at project root describes skills/channels/mcp/schedule.
- Optional build script parses this manifest instead of manual wiring.

## 13. Daily Cost Report Procedure

Use this when the user asks for a daily AI cost report from a cron or scheduled context.

### Data-source precedence
1. Provider billing APIs first, if they expose daily usage.
2. Local session telemetry second: read `state.db` for today’s sessions and aggregate `estimated_cost_usd`.
3. If both lack today’s spend, report `$0.00` explicitly and note the source/limitation.

### Cairo-day window rule
- Use Cairo local date: `datetime.now(ZoneInfo('Africa/Cairo')).date()`.
- Compute `start_ts = datetime.combine(date, time.min).replace(tzinfo=Cairo).timestamp()`.

### Cron-safe reporting rules
- State exact source for every number: `Nous billing state`, `state.db`, etc.
- If previous-day delta is unavailable, do not guess.
- If actual spend data is absent while estimated is zero, report both facts.

### Probe path for Nous provider
- `hermes_cli.nous_billing.get_billing_state()` gives `balanceUsd`, `monthlyCap.spentThisMonthUsd`.
- Local: `profile/state.db` table `sessions` has `started_at`, `model`, `api_call_count`, `estimated_cost_usd`, `actual_cost_usd`.

### Notes
- Do not conflate balance depletion with daily spend.
- For free-model cron traffic, expected daily spend is typically `$0.00`; report it plainly with source evidence.

See `references/nous_cost_report.md` for concrete queries and output snippets.

## 14. Verification Checklist

- [ ] Existing skills know their preferred model tier
- [ ] Dreaming cron exists and is scheduled
- [ ] Weekly brief cron exists for chosen channel
- [ ] Project directories exist under canonical paths (no legacy emoji paths in cron)
- [ ] OpenRouter health check passes
- [ ] Novel vault protected from cron edits
- [ ] Backup/archive behavior chosen (Obsidian + vault archive)
- [ ] Any cron intended to run on a non-default model is pinned via `jobs.json`, not only metadata
- [ ] All new external tools are recorded in `Tools/status.md` with repo, install state, and verification result
- [ ] Missing-source tools are explicitly marked `unknown` rather than fabricated
- [ ] Sensitive cron jobs include durable-session resume/checkpoint hooks
- [ ] Sensitive cron jobs use project-verifier.sh before delivery
- [ ] Critical ops require HITL approval gate before execution
