---
name: agentic-action-layer
description: >
  Converts an AI assistant from read-only RAG into guarded Agentic execution across local vaults,
  cron, messaging, terminal, and creative tools. Use when the user asks to make Lola/Dina/Hermes
  actually do things, not just answer; when they want an action allowlist, safety policy, or
  execution log; or when a session requires concrete artifacts instead of recommendations.
  Trigger phrases: اجعلها تنفذ، agentic، action layer، ارفع لـ agentic، ربط الإجراءات.
---

# Agentic Action Layer

## Definition
RAG = retrieve from knowledge base.
Agentic = choose and execute guarded actions.
This skill defines a repeatable pattern for adding an Action Layer to an assistant without weakening safety.

## Trigger
Apply when:
- the user asks to apply video/concept learnings as real automation
- the assistant needs to write files, create cron jobs, send messages, or run scripts
- a session moves from recommendation to execution

## Required Skeleton

1. `context/Action-Layer.md` — allowlist, guardrails, integration mapping
2. `scripts/action-layer.py` — router, safety filter, execution logger
3. Execution log at `context/execution-log.md`

## Guardrails Policy

### Read-only, no confirmation
- `vault.read`, `vault.search`, `web.fetch`, `summarize.transcript`, creative generation

### Requires confirmation
- `vault.write`, `vault.archive`, `vault.move`
- `terminal.command`, `code.run_python`, `script.run_safe`
- `msg.send_*`, `cron.create`, `cron.update`, `plugin.install`

### Forbidden
- destructive deletion outside archive flow
- edits outside allowed vault roots
- medical advice / seafood suggestions
- secret/token/password leakage in plaintext

## Python Router Pattern

Use a single router module per assistant:
- `plan_action(user_prompt)` returns `{status, action, needs_confirm, safety}`
- `check_safety(text)` blocks forbidden patterns
- `log_execution(record)` appends timestamped result to execution log
- Keep vault roots explicit per project so the same router can serve Lola and Dina

## Integration Mapping

Map action IDs to actual execution surfaces:
- vault → Obsidian/Hermes vault tools
- terminal/script → Hermes `terminal()` / `execute_code()`
- messaging → cron delivery + Telegram/Discord/Slack delivery targets
- cron → `cronjob(action='create')` with pinned model/provider
- image/tts → generate calls

## Execution Contract

When execution is requested:
1. Backup target if files may change.
2. Classify action and safety.
3. Execute or ask confirmation.
4. Write execution log.
5. Report real artifacts.

## Pitfalls
- Do not make every action auto-approve; start confirmation-required for writes and external sends.
- Do not invent integration endpoints; if webhook/credentials are missing, report blocker.
- Do not substitute fabricated tool output; if a tool fails, say so and stop.
