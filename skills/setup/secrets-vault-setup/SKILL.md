---
name: secrets-vault-setup
description: "API key/token intake, vault storage, and provider wiring for Hermes"
version: 1.0.0
author: Hafsa/Hermes
metadata:
  hermes:
    tags: [secrets, vault, openrouter, huggingface, setup]
---

# Secrets Vault Setup

Handle API keys and tokens from the user: store them in the vault, document provider models/aliases, and guide Hermes wiring without touching protected config files directly.

## Trigger

- User shares any API key/token: `OPENROUTER_API_KEY`, `HF_TOKEN`, `OPENAI_API_KEY`, etc.
- User asks to "add free models" or "add providers" to Hermes.

## Hard Rules

1. **Vault-first storage**: always persist keys to `/home/hatem/Documents/Hafsa-1/API_KEYS.md`.
2. **Config protection**: `~/.hermes/config.yaml` and `~/.hermes/.env` are write-protected from agent edits. Do not attempt `patch`/`write_file` on them. Use one of:
   - `hermes config set ...` from terminal
   - instruct the user to edit manually
3. **Alias docs**: for each provider, maintain a vault note with exact `model_aliases:` YAML.
4. **No plaintext leakage**: ask before echoing full secrets back into chat; save to vault instead.

## Workflow

### Receiving a token

1. Confirm provider and env var name.
2. Append to `API_KEYS.md` under provider heading. Include:
   - Key/token value
   - Provider slug
   - Env var name
   - Use case
3. Tell user: "Saved to vault. Next: add it to Hermes env."
4. Provide the exact terminal command or manual step:
   - `hermes config set model.api_key <key>` if applicable
   - OR: edit `~/.hermes/.env` and add `HF_TOKEN=hf_...`

### Adding free models

1. Choose known-free model IDs for the provider.
2. Create/update vault note `/home/hatem/Documents/Hafsa-1/OPENROUTER_FREE_MODELS.md` (or analogous HF note) with:
   - Table: alias, model ID, free flag
   - Copy-paste YAML block for `config.yaml`
3. If Hermes config already has `model_aliases:`, do not re-add. Only instruct user to merge any new entries.
4. Restart Hermes.

## Verification

```bash
# Check aliases loaded; do NOT print secrets
hermes chat -q "/model list" || true
```

## Pitfalls

- **Protected write**: `patch`/`write_file` on `~/.hermes/config.yaml` and `~/.hermes/.env` will be refused. Accept this and route around it.
- **Duplicate keys**: `API_KEYS.md` may accumulate duplicates over time; update in place rather than appending endlessly.
- **Model ID drift**: free model slugs change on OpenRouter. If a model errors, refresh the catalog rather than assuming alias syntax.

## Support Files

- `references/api-keys-template.md`
- `references/model-aliases-template.md`
