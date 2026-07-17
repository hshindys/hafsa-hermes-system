# Discord Gateway Conflict Debugging

When the Discord bot responds to slash commands (`/start`, `/sethome`) but never sends a response back to the server, the root cause is often a **dual-gateway conflict** — two Hermes instances running on the same host, both using the same Discord bot token.

## Symptoms

- Slash commands are received (logs show `slash '/start' invoked by user=...`)
- But no `Sending response` line follows the invocation
- The bot `Connects as BotName#XXXX` successfully
- The gateway process is running fine
- `restart counter` in `systemctl --user status` keeps growing (e.g., "at 18")

## Root Cause

Two or more Hermes gateway processes are running concurrently, both authenticating with the same Discord bot token:

```
PID 94662  hermes_cli.main gateway run           ← default profile
PID 95627  hermes_cli.main --profile hafsa gateway run  ← hafsa profile
```

The default profile gateway "wins" the token, causing the hafsa gateway's Discord interactions to silently fail.

## Diagnosis

```bash
ps aux | grep hermes | grep -v grep
```

If you see multiple `hermes_cli.main ... gateway run` processes (one without `--profile`, one with your named profile), you have a conflict.

## Fix

**Stop the conflicting gateway(s)** from a shell that is NOT inside any gateway process:

```bash
# Stop the default gateway (it has no --profile flag):
hermes gateway stop

# Or via systemctl:
systemctl --user stop hermes-gateway

# Then verify only your intended gateway is running:
ps aux | grep hermes | grep -v grep
```

**Check the restart counter keeps growing:**

```bash
systemctl --user status hermes-gateway-hafsa
```

Look for `Scheduled restart job, restart counter is at N` — if it keeps incrementing, the Discord connection is being unstable (sometimes a network issue, sometimes the conflict above).

## Discord Server Config: Bot Not Responding in Servers

If the bot works in DMs and with `@mentions` in servers but not in channels without mentioning:

```yaml
discord:
  require_mention: false   # Default is true — only responds when @mentioned
  free_response_channels: '<channel_id>'  # Comma-separated channel IDs for free response
  auto_thread: false       # Default true — auto-creates threads for responses, making them invisible in the main channel
```

Common fixes:
- `auto_thread: false` — stops the bot from responding inside invisible threads
- `require_mention: false` — let the bot respond in server channels without being mentioned
- `free_response_channels` — explicitly allow channels where the bot should respond freely

## After Config Changes

```bash
hermes -p <profile> gateway restart
```

Verify the gateway is stable:
```bash
systemctl --user status hermes-gateway-<profile>
```

The `restart counter` should stop growing at 0 or 1.
