---
name: discord-gateway-troubleshooting
description: "Use when Discord bot is not responding, not replying in server, or user mentions Discord connection issues. Covers: gateway conflicts (two processes), auto_thread issues, pairing/slash-command failures, require_mention config."
version: 1.0.0
author: Hafsa Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [discord, gateway, troubleshooting, bot-not-responding, auto-thread]
    related_tools: [hermes-agent, systematic-debugging]
---

# Discord Gateway Troubleshooting

## New Issue: `.env` Allowlist Blocking Inbound Commands

**Symptoms:** Bot connects and can send messages, but inbound slash commands / DMs are rejected with:
```
Unauthorized slash attempt: user=... reason='user not in DISCORD_ALLOWED_USERS / DISCORD_ALLOWED_ROLES'
```

**Root cause:** The Discord gateway enforces allowlists via env vars. If `DISCORD_ALLOWED_USERS` is missing from the profile `.env`, legitimate users can be rejected even when profile config says `allowed_users: '*'`.

**Fix:**
```bash
# Add missing Discord allowlist to profile .env
echo 'DISCORD_ALLOWED_USERS=<user_id>,<bot_id>' >> /home/hatem/.hermes/profiles/<profile>/.env

# Restart gateway from OUTSIDE the gateway process
hermes -p <profile> gateway restart
```

**Verification:**
```bash
cat /home/hatem/.hermes/profiles/<profile>/.env | grep DISCORD_ALLOWED_USERS
hermes -p <profile> pairing list
journalctl --user -u hermes-gateway-<profile>.service --since "10 min ago" | grep -i unauthorized
```

**Note:** Telegram uses `TELEGRAM_ALLOWED_USERS`; Discord uses `DISCORD_ALLOWED_USERS`. The two are independent. Do not assume one covers the other.

## Overview
Diagnose and fix Hermes Discord bot connectivity and response issues. Based on real debugging sessions with multi-gateway setups (Telegram + Discord).

## Common Issues & Fixes

### 1. Bot Not Responding in Server (Most Common)

**Root cause:** `require_mention: true` + `auto_thread: true` prevents responses outside threads.

**Fix sequence:**
```bash
# Check for conflicting gateway processes
ps aux | grep "hermes.*gateway" | grep -v grep

# If TWO gateways running with same token, kill the default one
# (the one without --profile flag)
kill <PID_of_default_gateway>

# Fix config: disable auto_thread, allow responses without mention
hermes -p <profile> config set discord.auto_thread false
hermes -p <profile> config set discord.require_mention false

# For multi-channel servers, set free_response_channels to the channel ID
hermes -p <profile> config set discord.free_response_channels "<channel_id>"

# Restart gateway from OUTSIDE the gateway process
hermes -p <profile> gateway restart
```

**CRITICAL:** Never run `hermes gateway restart` from inside the gateway process — it will refuse with "Refusing to restart the gateway from inside the gateway process. Run from a separate shell."

### 2. Two Gateway Processes Running Simultaneously

**Symptoms:** Discord connects but doesn't respond, or connect/disconnect loops in logs.

**Diagnosis:**
```bash
ps aux | grep "hermes_cli.*gateway"
# Look for: one with --profile flag, one without
```

**Fix:** Kill the default (non-profile) gateway. The profile gateway should own the token.

### 3. Discord Slash Commands Registering But Not Responding

**Symptoms:** `/start`, `/sethome` appear in logs as "invoked" but no response sent.

**Root cause:** Either gateway conflict (see #2) or auto_thread routing responses to invisible thread.

**Fix:**
1. Ensure only ONE gateway process runs
2. `discord.auto_thread: false`
3. `discord.require_mention: false` (for servers)
4. Check logs for `[Discord] Sending response` — if missing, gateway conflict

### 4. Discord Pairing Not Working

**Fix:**
```bash
# Approve pairing
hermes -p <profile> pairing approve discord <pairing_code>

# Verify
hermes -p <profile> pairing list
```

### 5. Connect/Disconnect Loop in Logs

**Symptoms:** `✓ discord connected` followed by `✓ discord disconnected` every few minutes.

**Root cause:** Network instability or token conflict.

**Fix:**
1. Ensure single gateway process
2. Check network/firewall for Discord API (discord.com/api)
3. Verify token in `.env` is correct and not expired

### 6. Discord LoginFailure: Improper Token

**Symptoms:** Logs show `LoginFailure: Improper token has been passed`.

**Root cause:** The stored `discord.token` in the profile config is invalid/expired/reset.

**Fix:**
1. Get a fresh token from the Discord Developer Portal.
2. Update config: `hermes -p <profile> config set discord.token '<NEW_TOKEN>'`.
3. Restart the gateway from a separate shell: `hermes -p <profile> gateway restart`.

## Key Discord Config Reference

```yaml
discord:
  require_mention: false        # Respond without @ mention
  auto_thread: false             # Don't auto-create threads
  free_response_channels: ''     # Channel IDs for free responses
  allowed_channels: ''           # Empty = all channels
  history_backfill: true
  reactions: true
```

## Default Profile Gateway Service

On Fedora/systemd:
```bash
# Stop default gateway (lets profile gateway work alone)
systemctl --user stop hermes-gateway

# Or kill the specific PID
kill <PID>
```

Note: Default gateway will respawn via systemd if not disabled:
```bash
systemctl --user disable hermes-gateway
```

## Verification Checklist

- [ ] Only ONE gateway process running (`ps aux | grep gateway`)
- [ ] `auto_thread: false` in config
- [ ] `require_mention: false` for server use
- [ ] Logs show `[Discord] Sending response` (not just "slash invoked")
- [ ] `hermes -p <profile> pairing list` shows approved users
