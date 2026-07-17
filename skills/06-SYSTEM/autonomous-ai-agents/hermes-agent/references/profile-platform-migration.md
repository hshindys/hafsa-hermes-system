# Profile Platform Migration: Taking Over Discord/Telegram from Default

When a user wants a named profile (e.g. `hafsa`) to take over platform ownership from the `default` profile, the migration involves understanding token locks, gateway conflict resolution, and verification. This is a common setup step when users create their first named profile and want it to be their primary agent.

## Trigger Conditions

- User asks to "let profile X take over Discord/Telegram"
- User asks to "stop default and use profile X"
- User reports that a platform is connected to the wrong profile
- Two profiles compete for the same bot token

## How Platform Ownership Works

### Token-Lock Mechanism

Hermes uses a **token-lock** system: only one gateway process can bind to a given bot token at a time. When Profile A's gateway connects with a Telegram/Discord bot token, Profile B's gateway **cannot** connect with the same token — it gets:

```
ERROR: telegram: Telegram bot token already in use (PID XXXXX). Stop the other gateway first.
```

This is a **safety feature**, not a bug. It prevents two agents from responding to the same messages.

### The Migration Sequence

1. **Default profile was running first** — it connected to both Discord and Telegram using tokens from `~/.hermes/.env`
2. **Named profile starts** — it reads the **same** `.env` (or its own `.env` with the same tokens) and tries to connect
3. **Initial conflict** — the named profile's gateway fails with "token already in use"
4. **Default gateway releases** — when the default gateway stops (manually or because it loses the race), it disconnects from platforms
5. **Named profile reconnects** — it successfully binds the tokens and takes over

## Step-by-Step Migration Procedure

### 1. Verify Current State

```bash
hermes profile list
```

Look at which profile's gateway is `running` vs `stopped`.

### 2. Check Both Gateways' Logs

```bash
# Default profile logs
grep -E "✓ discord|✓ telegram|✗ discord|✗ telegram|token already in use" ~/.hermes/logs/gateway.log | tail -10

# Named profile logs
grep -E "✓ discord|✓ telegram|✗ discord|✗ telegram|token already in use" ~/.hermes/profiles/<name>/logs/gateway.log | tail -10
```

### 3. Stop the Default Profile's Gateway

```bash
hermes gateway stop
# or, if default gateway was already stopped, nothing to do
```

### 4. Start the Named Profile's Gateway

```bash
hermes -p <name> gateway start
# or, using the alias:
<name> gateway start
```

### 5. Verify Takeover

```bash
hermes profile list
```

Confirm the named profile shows `running`.

Check logs for successful connection:
```bash
grep -E "✓ discord|✓ telegram" ~/.hermes/profiles/<name>/logs/gateway.log | tail -5
```

### 6. Verify Platform Functionality

- Send a test message on Telegram
- Send a test message on Discord
- Confirm responses come from the named profile (check bot identity)

## Diagnostic Patterns

### "Both profiles are competing"

If both gateways are running and both trying to use the same tokens:
```
ERROR: Gateway hit a non-retryable startup conflict: telegram: Telegram bot token already in use (PID XXXXX). Stop the other gateway first.
```

**Fix**: Stop the profile you don't want running:
```bash
hermes gateway stop   # stops default
```

### "Named profile connected but default is still running"

This shouldn't happen with token-locking. If it appears to, check:
- Are they using **different** bot tokens? (check `.env` files)
- Is the default gateway actually bound to a different account?

### "I want different profiles for different platforms"

This requires **different bot tokens** per profile:
1. Create a new bot on Discord Developer Portal / Telegram BotFather
2. Put Profile A's token in `~/.hermes/profiles/A/.env`
3. Put Profile B's token in `~/.hermes/profiles/B/.env`
4. Each profile can now run simultaneously without conflict

## Post-Migration: Discord Config Fix

After the named profile takes over Discord, the bot might still not respond
in server channels if `require_mention` was `true` or `auto_thread` was
enabled (both are defaults).

### Symptoms After Migration

- Slash commands are received (`slash '/start' invoked by user=...`)
- No `Sending response` follows the invocation
- Bot responds in DMs but not in server channels
- `auto_thread: true` makes responses land in invisible threads

### Fix

```bash
hermes -p <profile> config set discord.require_mention false
hermes -p <profile> config set discord.auto_thread false
hermes -p <profile> config set discord.free_response_channels "<channel_id>"
```

Restart after config changes:
```bash
hermes -p <profile> gateway restart
```

## Key Insight

**Profiles don't "own" platforms in config** — they own them by holding the token-lock. The migration is fundamentally about transferring token access from one gateway process to another, not about editing a config setting.

## Common Pitfall

Don't try to run two gateways with the same bot token simultaneously. The token-lock will refuse the second one. If you need both profiles online, they need **separate bot tokens**.
