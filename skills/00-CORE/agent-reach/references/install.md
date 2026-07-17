# Agent Reach — Installation Guide (Linux/macOS)

When the user asks to install or set up Agent Reach, follow this guide.

## Install Methods

### Method 1: pipx (preferred, if available)

```bash
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

### Method 2: venv (when pipx is missing or PEP 668 blocks pip)

```bash
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

> ⚠️ **Do NOT** use `sudo`. Do NOT install outside `~/.agent-reach/`.

### Post-install: Activate the skill in Hermes

After installing Agent Reach, copy the auto-generated skill to the active profile's skills directory:

```bash
# Find the installed skill
find ~/.agents/skills -name "SKILL.md" -path "*agent-reach*" 2>/dev/null
# Or check the installer output for the exact path

# Copy to active profile (e.g. hafsa)
cp -r ~/.agents/skills/agent-reach ~/.hermes/profiles/hafsa/skills/agent-reach

# Restart gateway to pick up the new skill
# (Run from a terminal OUTSIDE the gateway process)
# hermes -p hafsa gateway restart
```

> ⚠️ **Restart caveat**: `hermes gateway restart` cannot be called from inside the running gateway process — it will refuse with "Refusing to restart the gateway from inside the gateway process." Always tell the user to run the restart from their terminal.

## What `agent-reach install --env=auto` Sets Up

- **Zero-config channels** (no login needed): Web (Jina Reader), YouTube, GitHub, RSS, Exa Search, V2EX, Bilibili (basic)
- **Login-backed channels** (need browser cookies): Twitter/X, Reddit, XiaoHongShu, 小红书
- **Optional channels**: 雪球 (stocks), LinkedIn, 小宇宙播客 (podcast transcription)

## Verify Installation

```bash
source ~/.agent-reach-venv/bin/activate  # if using venv method
agent-reach doctor --json
```

Expected: 11/13 channels ✅ (雪球 and LinkedIn need extra setup).

## Common Pitfalls

1. **Forgetting to activate venv**: If `agent-reach: command not found`, run `source ~/.agent-reach-venv/bin/activate` first.
2. **Trying to restart gateway from inside gateway**: The command will be blocked. Tell user to run from their terminal.
3. **Not copying skill to profile**: The skill installs to `~/.agents/skills/` but Hermes profiles read from `~/.hermes/profiles/<name>/skills/`. Must copy manually.
4. **PEP 668 on macOS/Homebrew**: Use pipx or venv. Do NOT use `pip install --user`.
