---
name: hermes-provider-management
description: "Add, verify, switch, and troubleshoot LLM providers in Hermes — OpenRouter, custom endpoints, NVIDIA, Anthropic, and others. Use when user reports provider auth failures, asks to make a provider/model default, or wants to integrate a new API endpoint."
version: 1.0.0
author: Hafsa/Hermes
license: MIT
---

# Hermes Provider Management

Covers provider setup, default model switching, auth troubleshooting, and custom endpoint integration for Hermes Agent.

## Quick Decision Tree

1. **"make X model default"** or **"provider auth failed"** → go to "Setting Default Provider"
2. **"integrate NVIDIA / custom API"** → go to "Custom Endpoint Setup"
3. **Auth errors persist after config change** → go to "Auth Troubleshooting"

---

## Setting Default Provider

### 1. List current auth
```bash
hermes auth list
```

### 2. Check current model config
```bash
hermes config show model
```

### 3. Set provider + model
```bash
hermes config set model.default <provider>/<model>
hermes config set model.provider <provider_name>
```

Examples:
```bash
hermes config set model.default openrouter/anthropic/claude-sonnet-4
hermes config set model.provider openrouter

hermes config set model.default minimaxai/minimax-m3
hermes config set model.provider custom
hermes config set model.base_url https://integrate.api.nvidia.com/v1
hermes config set model.api_key nvapi-...
```

### 4. Restart to apply
- Gateway: `hermes gateway restart` from terminal
- CLI: exit and relaunch (`/reset` inside session is NOT enough for provider changes)

---

## Custom Endpoint Setup

When a user provides an API script for a provider not natively listed:

1. Confirm the endpoint supports OpenAI-compatible `/v1/chat/completions`
2. Set `model.provider: custom`
3. Set `model.base_url` to the API root (not the full chat completions path)
4. Set `model.default` to the model ID string the provider expects
5. Set `model.api_key` with the bearer token
6. Restart gateway/CLI

### Verification
```bash
hermes config show model
hermes chat -q "ping" --provider custom --model <model_id>
```

---

## Auth Troubleshooting

### Credential file protection
- `~/.hermes/.env` and credential stores may reject direct edits/writes from agents
- **Use `hermes config set` and `hermes auth add` instead of editing `.env` directly**
- Direct file edits to protected credentials will fail with "Access denied" / "Write denied"

### Common fixes
1. Re-add credential: `hermes auth add <provider>` or `hermes auth add <provider> --no-browser`
2. Check logs: `grep -i "auth\|failed\|error" ~/.hermes/logs/gateway.log | tail -30`
3. Verify env var name matches provider table in hermes-agent skill
4. For OpenRouter: ensure `OPENROUTER_API_KEY` matches the actual key
5. After ANY config change: restart gateway, not just `/reset`

### Token conflict (Discord)
- Two profiles using same bot token causes restart loops
- Check: `grep -i "token already in use" ~/.hermes/logs/gateway.log`
- Fix: stop other profile or use different tokens per profile

---

## Provider Reference

| Provider | Env var | Notes |
|----------|---------|-------|
| OpenRouter | `OPENROUTER_API_KEY` | Router to 300+ models |
| Anthropic | `ANTHROPIC_API_KEY` | Direct |
| NVIDIA NIM | custom endpoint | OpenAI-compatible, use `custom` provider |
| Google Gemini | `GOOGLE_API_KEY` or `GEMINI_API_KEY` | |
| xAI/Grok | `XAI_API_KEY` | |
| DeepSeek | `DEEPSEEK_API_KEY` | |
| Nous Portal | OAuth via `hermes auth` | |

---

## Pitfalls

- **`/reset` ≠ restart.** Provider/model/MoA changes need `hermes gateway restart` from a terminal outside the gateway process. Restarting from inside the running session is blocked.
- **`.env` is often write-protected.** Direct edits can be rejected or silently ignored by Hermes’s config system. Prefer `hermes config set` for provider/api-key/model fields.
- **Duplicate env vars hide each other.** Hermes may only read the last or first occurrence. If `OPENROUTER_API_KEY` appears more than once, dedupe it before troubleshooting auth; a single clean line avoids 401s that look like “credentials are wrong”.
- **Changing provider does not override base_url, default, or disabled_toolsets by itself.** Set them explicitly after switching: `hermes config set model.base_url ''`, `hermes config set model.default <provider>/<model>`, and `hermes config set disabled_toolsets '[]'` (or `'["moa"]'` if disabling MoA).
- **Base URL is API root, not full path.** Use `https://integrate.api.nvidia.com/v1`, not `.../chat/completions`.
- **Config edits by hand can be overwritten.** Prefer `hermes config set` over raw YAML edits.
