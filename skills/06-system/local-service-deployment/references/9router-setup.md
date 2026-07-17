# 9Router Setup Reference

## What it is
`9router` is a local LLM router/gateway. It exposes an OpenAI-compatible endpoint and routes requests across multiple providers/models using ordered combos with automatic fallback.

## Install
```bash
npm install -g 9router
```

## Run
```bash
9router --host 127.0.0.1 -n -l
# or background/tray mode
9router --host 127.0.0.1 -n -t
```

Default dashboard: `http://127.0.0.1:20128`
Default password: `123456` — change on first login.

## Verified behaviors
- Binds to `127.0.0.1:20128` when `--host 127.0.0.1` is passed.
- Without `-t`/tray mode, the process can exit immediately after startup even if the server briefly comes up.
- With `-t`, it stays running in background with tray semantics.
- DB path: `/home/hatem/.9router/db/data.sqlite`

## Integration points
- Use the dashboard to add providers and create combo fallback chains.
- Point downstream tools to `http://127.0.0.1:20128/v1` with the router API key.
- Combo name is used as the model target in client `settings.json`/endpoint configs.
