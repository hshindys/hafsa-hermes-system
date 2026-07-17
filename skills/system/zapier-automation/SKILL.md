---
name: zapier-automation
description: MUST USE when user asks about Zapier integrations, zaps, webhooks, or no-code automations. Bridges Hermes to Zapier when ZAPIER_API_KEY is configured.
metadata:
  version: 0.1.0
  profile: hafsa
---

# Zapier Automation

## Boundary
Zapier is for automations, not for bypassing external platform blocks. A Zap cannot retrieve YouTube transcript/captions from a network that YouTube is blocking.

## Setup
1. Get API key from https://zapier.com/app/api
2. Export key: `export ZAPIER_API_KEY=***`

## Usage
```bash
zapier list zaps
zapier trigger <zap_id>
```

## Target format
Use explicit targets: `telegram:<chat_id>`, `slack:C<channel_id>`, `discord:<channel_id>`, or `origin`. Generic platform names without explicit target may fail delivery.

## Planned automations
- Daily brief → Telegram/Discord
- Vault index updates → Zap
- Health reminders → push notifications

## Fallback behavior
If `cronjob` delivery to a platform target fails, prefer reading content from disk and emitting it manually rather than retrying indefinitely.
