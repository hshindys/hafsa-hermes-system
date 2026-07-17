---
name: local-service-deployment
description: Install and run local services or automation tools (n8n, etc.) with a docker-first, package-manager-fallback pattern. Use when deploying, starting, or verifying local services on this host.
---

# Local Service Deployment

## Trigger
- User asks to install/run a local service: n8n, 9Router, or similar Node-based automation/AI servers.
- Docker path fails or is unavailable; fallback to npm or direct binary.

## Primary Pattern
1. **Probe environment**
   - Check daemon/binary availability first.
   - Example: `docker compose version`, `command -v docker`, `command -v <tool>`.

2. **Preferred: containerized deploy**
   - Write `docker-compose.yml` with env + volume mount for persistence.
   - `docker compose up -d` from a dedicated project dir.
   - If the docker daemon is missing, switch to fallback immediately; do not loop.

3. **Fallback: native install**
   - Prefer global install when the tool is a CLI/server.
   - For Node tools: `npm install -g <pkg>`.
   - For Python tools: `pip install --user <pkg>` or a venv.
   - Use `terminal(background=true, notify_on_complete=true)` for installs that exceed ~60s.
   - Use `process(action='poll')` for quick status checks; do not spam polls.

4. **Config style**
   - Keep service config in env vars or a single `.env` in the project dir.
   - Avoid interactive setup; choose deterministic settings (sqlite, http, localhost webhook).

5. **Start service**
   - Use `terminal(background=true)` to start long-lived services.
   - Set `notify_on_complete=true` so startup completion surfaces automatically.
   - Do not use `nohup`/`disown` wrappers; let Hermes track the background process.

6. **Readiness verification**
   - Check port is listening: `ss -ltnp | grep :<port>`.
   - Probe HTTP: `curl -sS -o /dev/null -w '%{http_code}' http://localhost:<port>/`.
   - Expect `200` before declaring success.

7. **Report**
   - Give the access URL and exact port.
   - Mention storage path and any next-step options (auth, first workflow).

## Pitfalls
- Docker daemon may be installed but not running; `docker` is in PATH but `/var/run/docker.sock` is absent. Detect this fast and fall back.
- npm global installs of large Node apps can take 5–10 minutes. Use background mode from the start.
- Don't block the main turn on long installs; continue with readiness prep in parallel.
- Some Node packages expose on all interfaces by default. Bind explicitly to `127.0.0.1` unless the user needs LAN access.
- A service can start and immediately exit if no explicit foreground/runtime flag is used. For UI servers like 9Router, use tray/background mode to keep it alive.
- Startup output can be misleading: a service may show `Ready` and then exit. Always validate with both port check and HTTP `200` probe before declaring success.
- For transient dashboard/API unreachable errors after supposedly successful startup, treat it as “started then exited” and restart in tray/background mode instead of retrying the same launch style.
