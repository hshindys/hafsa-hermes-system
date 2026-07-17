---
name: hermes-interpreter-pinning
description: "Pinning Hermes upgrades to a compatible Python interpreter when the system Python is newer than the release requires. Covers venv creation, wrapper rewrites, and resolver conflict diagnosis."
version: 1.0.0
author: Hafsa/Hermes
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, setup, upgrade, python, venv, packaging]
    related_skills: [hermes-agent]
---

# Hermes Interpreter Pinning

When the running/default Python is newer than a Hermes release supports, `pip install -U hermes-agent` may downgrade rather than upgrade, and `hermes update` may stall or time out. This skill teaches the durable repair: isolate the compatible interpreter in a dedicated venv and point the `hermes` wrapper to it.

Rule of thumb: if the release you want says `Requires-Python >=3.11,<3.14` and you’re on Python 3.14, stop and use this skill.

## Verification

```bash
hermes --version
python3 --version
pip show hermes-agent | grep -E 'Name|Version|Requires-Python'
python3.11 --version
```

If `hermes --version` is older than expected after upgrade attempts, continue.

## Repair Sequence

### 1. Inspect current layout
```bash
ls ~/.hermes/hermes-agent/
systemctl --user status hermes-gateway-<profile> --no-pager 2>/dev/null || true
```
Stop any running gateway for the profile before mutating the wrapper. New venv + install avoids touching the running process.

### 2. Create a pinned venv
```bash
python3.11 -m venv ~/.hermes/hermes-agent/venv-h18
```
Adjust the suffix if pinning to a different release line.

### 3. Install inside the venv
```bash
~/.hermes/hermes-agent/venv-h18/bin/python3.11 -m pip install --upgrade 'hermes-agent==TARGET_VERSION'
```
Use the venv interpreter directly; do not use `pip install --user` on PEP 668 managed installs.

### 4. Rewrite the wrapper
```bash
cat > ~/.local/bin/hermes <<'EOF'
#!/usr/bin/env bash
exec ~/.hermes/hermes-agent/venv-h18/bin/python3.11 -m hermes_cli.main "$@"
EOF
chmod +x ~/.local/bin/hermes
hash -r
```

### 5. Lock the effective runtime
```bash
hermes --version
```
If this still looks wrong, compare `which hermes` and `readlink -f $(which hermes)`.

## Why this works
- The venv sits on an interpreter Hermes supports, bypassing the system Python mismatch.
- The wrapper substitutes `/usr/bin/python3` with an explicit venv interpreter, so every caller gets the pinned runtime.
- The Hermes project path (`~/.hermes/hermes-agent/`) is unchanged; only the execution env changes.

## Pitfalls
- Do not run `hermes update` as the sole path when the release is incompatible with the active interpreter — it downgrades instead of upgrading.
- Do not use `pip install --user` on externally managed system Python for the target release; the resolver blocks it or locks to older versions.
- If multiple profiles share the same `~/.local/bin/hermes`, this wrapper applies globally — confirm before overwriting.
## Extensions

- For multi-profile setups, create per-profile wrappers under `~/.local/bin/` such as `hermes-hafsa`, `hermes-hatem`, and alias the user’s shell accordingly.
- For automated recovery, a cron/noop job can run the verification command and alert if the pinned venv is missing or the version drifts.
- Use the pinned venv as the universal install target for extras that need newer packaging tooling: TTS/voice-cloning stacks (`omnivoice`, `voicetut-tts`), local inference deps (`torch`, `torchaudio`, `transformers`, `peft`, `onnxruntime`), and anything else blocked by system Python/PEP 668. Run them with the venv interpreter explicitly.
- If the venv build backend complains about `setuptools.backends`, upgrade `setuptools` and `wheel` inside the venv first; if the repo still fails to build, fall back to `pip install` from PyPI or an offline stub instead of blocking on first-run model downloads.
- Offline fallback pattern for voice features: create a thin wrapper script in `~/.local/bin/` that prefers the real provider, then falls back to `espeak-ng`/`flite` for Arabic stub TTS. This decouples “voice output works” from “the fancy model is already downloaded.”

## References
- PEP 668: https://peps.python.org/pep-0668/
- Hermes packaging pins: inspect `pyproject.toml` `Requires-Python` inside the installed wheel when diagnosing.
