---
name: messaging-platform-setup
description: "Configure and troubleshoot Hermes messaging platforms (Slack, Discord, Telegram). Covers required env vars, config.yaml sections, systemd/.env loading, OAuth/Socket Mode, Event Subscriptions, verification, and common connection errors."
version: 1.0.0
---

# Messaging Platform Setup

Use this skill when setting up or fixing Hermes messaging integrations. It covers the exact config Hermes expects, how the gateway loads `.env`, and the platform-specific prereqs for Slack, Discord, and Telegram.

## Core rules (all platforms)

- Env vars and behavior are split correctly: secrets go in `.env`, settings go in `config.yaml`.
- Confirm token prefix first using a direct Slack/Discord auth test when possible.
- Runtime visibility: when terminal/gateway output redacts secrets, inspect the source file directly instead of trusting masked CLI output.
- When the service is managed by systemd, Hermes only inherits env vars that systemd loads. If your edit to a profile `.env` isn't taking effect, create or update a service drop-in:  
  `/home/hatem/.config/systemd/user/hermes-gateway-<profile>.service.d/env.conf` with:

  ```ini
  [Service]
  EnvironmentFile=/home/hatem/.hermes/profiles/<profile>/.env
  ```

  Then run `systemctl --user daemon-reload && systemctl --user restart hermes-gateway-<profile>` and verify via `journalctl`.

## Slack (Socket Mode required by Hermes on Fedora)

### Slack app prerequisites (do once)
1. Open https://api.slack.com/apps and select the app.
2. **OAuth & Permissions** → add bot token scopes:
   - `chat:write`
   - `im:read`, `im:write`, `im:history`
   - `channels:history`
3. **Event Subscriptions** → enable events:
   - `message.im` (DM)
   - `message.channels` (public channels)
4. **Socket Mode** → enable → copy **App-Level Token** (`xapp-...`).
5. Reinstall/update workspace permissions if prompted.

### Hermes Slack config
Add to `~/.hermes/config.yaml`:

```yaml
slack:
  bot_token: "${SLACK_BOT_TOKEN}"
  home_channel: "${SLACK_HOME_CHANNEL}"
  mode: dm+channels          # or dm|channels
  require_mention: true      # true in public channels
  allowed_channels: []
  enabled: true
```

Profile `.env` must include:
```bash
SLACK_BOT_TOKEN=xoxb-....ERS=    # optional comma-separated user IDs
```

Note: The bot token format must start with `xoxb-`.

### Verification
```bash
hermes gateway restart
journalctl --user -u hermes-gateway-hafsa -n 60 | grep -Ei 'slack connected|slack failed|SLACK_APP_TOKEN|SLACK_BOT_TOKEN|messaging platforms'
```

### Common errors
- `[Slack] SLACK_APP_TOKEN not set` → `.env` not loaded or token line malformed/missing.
- `[Slack] SLACK_BOT_TOKEN not set` → bot token missing or redaction masked a bad write.
- `not_authed` from `auth.test` → token revoked or wrong bot/app.
- “Sending messages to this app has been turned off” → one or more of: Event Subscriptions not enabled, missing `message.im`/`message.channels`, or the app isn’t installed to the workspace after adding scopes.

## Discord quick checklist

- `config.yaml` must contain discord config under plugin or top-level.
- Enable **Message Content Intent** in Discord developer portal.
- If you see 401, regenerate token and update `.env`.

## Telegram quick checklist

```yaml
telegram:
  bot_token: "${TELEGRAM_BOT_TOKEN}"
  home_channel: "${TELEGRAM_HOME_CHANNEL}"
  allowed_users: "${TELEGRAM_ALLOWED_USERS}"
```

## Multi-platform delivery

Cron jobs can deliver to more than one destination using comma-separated targets:

```yaml
deliver: "slack:#exec-brief,telegram"   # Slack channel + Telegram DM
deliver: "telegram,discord"             # both chats
deliver: "slack:#alerts,origin"         # Slack channel + also keep origin
deliver: "all"                          # every connected home channel
```

Order does not imply priority; the message is posted to each destination independently.

## Model drift breaks unpinned cron jobs

After a global provider/model change, unpinned cron jobs can stop executing with:

`RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created ...`

Fix: pin the job explicitly right after creation:

```bash
cronjob action=update job_id=<id> provider=<provider> model=<model>
```

Preventive rule: whenever you create or reuse a cron job that uses an LLM prompt, update it with `provider` and `model` immediately so it does not drift later.

## Verification commands

```bash
hermes status --all
systemctl --user status hermes-gateway-<profile>
hermes gateway restart
```

When bot-token writes look correct in chat but Hermes still says missing, it is a strong signal that `.env` is not being loaded by systemd or the write did not persist. Fix that before editing config again.