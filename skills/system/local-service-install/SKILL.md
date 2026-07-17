---
name: local-service-install
description: Install and start local services/workflows on the current workstation. Prefer simplest viable path, verify before waiting, and background long installs.
trigger: |
  Use when the user asks to install, launch, or verify a local service/tool
  (n8n, databases, dev servers, daemons) on this machine.
---

# Local Service Install
How to set up and verify local services for this user fast.

## Method preference
1. Docker Compose — only if `docker compose` exists AND daemon is reachable.
2. Global npm/pip/gem/binaries — simplest isolation, easy rollback.
3. Source/clone — last resort.

## Steps
- **Check env first**: which docker / docker compose / runtime versions.
- **Verify daemon**: `docker info` or equivalent before assuming Docker works.
- **Long installs**: background immediately with `notify_on_complete=true`.
- **Start**: foreground short command, background daemons with restart: always.
- **Health check**: curl http://localhost:<port>/health or equivalent.
- **Report**: exact URL, port, next step; no explanations unless asked.

## Pitfalls
- Don’t assume Docker is usable; `docker compose up` fails silently if daemon is down.
- Don’t wait 5 minutes on foreground install when background+notify is expected.
- Don’t cleanup or revert after success unless asked.
- Don’t propose paid/hosted alternatives when local is free and trivial.
- Some Rust/Terminal Linux repos depend on vendored Zig/libghostty-vt; `cargo build --release` can fail on clean Fedora boxes without Zig. Fallback: use GitHub Releases/Latest assets and install the prebuilt static binary when the project publishes one. Verify with `--version` after install.
- For bundled macOS GUI binaries on Linux hosts, do not attempt to run them; if the user needs it, note it and only install when on a supported host.

## References
- `references/herdr-linux-binary.md` — tested binary-install workflow for herdr on Fedora/Linux when Zig is absent.
- `references/n8n-compose.yml` for a known-good local n8n compose file.
- `references/verify-running.sh` for port-and-process checks.
