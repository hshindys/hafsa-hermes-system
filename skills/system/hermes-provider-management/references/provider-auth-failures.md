# Provider Auth Failure Reference


## Symptom Checklist

- `auth list` shows only 1 credential → likely env/duplication issue on read
- API works with `curl` → key is valid, issue is in Hermes env/config chain
- Logs show `HTTP 401: User not found` → key being passed wrong or as `None`
- Logs show `401` on a model you didn’t select → an override or fallback is silently keeping an old model assignment


## Duplicate OPENROUTER_API_KEY Pattern

**Root cause:** Hermes profile `.env` had two `OPENROUTER_API_KEY` lines. The first was a corrupted/broken mixed line. Hermes was passing the malformed value to OpenRouter, causing a `401` while `curl` with the same raw key succeeded.

**Fix:**
1. Dedupe `.env` → only one clean `OPENROUTER_API_KEY=*** Restart gateway externally (`systemctl --user restart ...`)


## MoA Staying Visible After Disable

**Root cause:** `disabled_toolsets` protects the runtime feature, but the config change requires a full external gateway restart to take effect.

**Fix:**
```bash
hermes config set disabled_toolsets '["moa"]'
hermes gateway restart   # from outside the running session
```


## Forcing OpenRouter Model After Provider Change

Switching `model.provider` is not enough if the default model or base URL was touched earlier. Force a clean trio:
```bash
hermes config set model.provider openrouter
hermes config set model.default stepfun/step-3.7-flash:free
hermes config set model.base_url ''
hermes gateway restart
```


## Gateway Restart Rule of Thumb

Changes that require an external restart:
- `model.provider`
- `model.default`
- `model.base_url`
- `disabled_toolsets`

Changes that do NOT need external restart:
- Memory/vault changes
- Cron job edits (take effect on next tick)
