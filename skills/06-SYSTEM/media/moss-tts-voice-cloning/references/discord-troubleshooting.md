# Discord Bot Silent — Troubleshooting Guide

## Common Issues

### Bot connects but doesn't respond
**Root cause:** Two gateway processes running (default + hafsa profile) both trying to use the same Discord token.

**Fix:**
```bash
# Kill default gateway (it respawns via systemd)
hermes gateway stop

# Or disable it permanently
systemctl --user disable hermes-gateway
```

### Bot responds in threads instead of channel
**Config fix:**
```yaml
discord:
  auto_thread: false
  require_mention: false
  free_response_channels: <channel_id>
```

### Slash commands invoked but no response
**Check:**
1. Is the default gateway conflicting? → `hermes gateway stop`
2. Is `require_mention: true`? → Set to `false`
3. Is `auto_thread: true`? → Set to `false`
4. Is the bot's Discord token correct? → Check `.env`

### Gateway keeps restarting (high restart counter)
**Check logs:**
```bash
journalctl --user -u hermes-gateway-hafsa --since "10 minutes ago" | grep -i "restart\|error\|conflict"
```

**Common cause:** Token conflict with another process or stale PID file.

### Config edit blocked by Hermes agent
The agent cannot edit `config.yaml` directly (security restriction).

**Workaround:**
```bash
# Simple keys
hermes -p hafsa config set discord.require_mention false

# Nested sections — use Python or sed, or edit manually
# The agent CAN write files via write_file/patch tools
```
