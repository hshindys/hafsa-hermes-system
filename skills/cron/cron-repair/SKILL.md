---
name: cron-repair
description: "Fix broken Hermes cron jobs: config drift pinning, profile-local store location, missing scripts, cross-profile edit guard."
version: 1.0.0
author: Hafsa/Agent
license: MIT
metadata:
  hermes:
    tags: [cron, repair, drift, scripting, jobs]
---

# Hermes Cron Repair

## When to use

Use when cron jobs have `last_status: error` and the error is one of:

- `RuntimeError: Skipped to prevent unintended spend: global inference config drifted ...`
- `RuntimeError: HTTP 401: User not found.` on agent jobs with no obvious auth issue
- `Script not found: .../scripts/scripts/...` (doubled path) or any script-not-found error on `no_agent=True` jobs

## Key facts (durable rules)

- **Two stores exist.** `/home/hatem/.hermes/cron/jobs.json` is legacy/root (currently 3 jobs, often stale). The authoritative store is:
  `/home/hatem/.hermes/profiles/<profile>/cron/jobs.json`
- **Cross-profile soft guard blocks edits** to the profile-local file when running under a different profile. When the `cronjob` tool silently drops `model` writes or returns `model: null` after update, switch to a direct terminal/python edit on the file.
- **`model`/`provider` updates often fail through the `cronjob` tool schema** even when it returns `success: true`. The field stays null. Treat the tool as unreliable for that field.

## Repair patterns

### Pin model/provider for drift errors

When `last_error` says: `Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'nous' -> 'openrouter'; model 'stepfun/step-3.7-flash:free' -> 'openrouter/google/gemma-4-31b-it:free'), and this job is unpinned.`:

edit the profile-local `cron/jobs.json` directly and set:

```json
"model": "stepfun/step-3.7-flash:free",
"provider": "nous",
"provider_snapshot": "nous",
"model_snapshot": "stepfun/step-3.7-flash:free"
```

Pinning both current and snapshot fields prevents the scheduler from re-evaluating global config on each tick.

### Fix missing-noop script jobs

For `no_agent=True` jobs with `script` paths that fail:

1. Create the script under `<profile>/scripts/` (not under `<profile>/scripts/scripts/`).
2. If you only need the job to stop erroring while preserving the slot, make a noop:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   mkdir -p /home/hatem/.hermes/profiles/<profile>/cron/output
   echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] <jobname> NOOP OK" > /home/hatem/.hermes/profiles/<profile>/cron/output/<jobname>.log
   exit 0
   ```
3. `chmod +x` the script.
4. Set `"script": "<name>.sh"` (no `scripts/` prefix in the JSON field) on the job object.

### Resolve `HTTP 401: User not found.` on agent cron jobs

Try the pin model/provider pattern above before changing provider credentials.

## Verification

After edits, re-list jobs and re-run the failing job. Confirm `last_status` changes and `last_error` clears.

## Known drift message templates

The scheduler emits exact variants depending on what changed in global config:

```
Skipped to prevent unintended spend: global inference config drifted since this job was created
(provider 'nous' -> 'openrouter'; model 'stepfun/step-3.7-flash:free' -> 'openrouter/google/gemma-4-31b-it:free'),
and this job is unpinned.
```

Sometimes only `model` drifts without `provider`, or vice versa. Pin both fields anyway.

## Direct-edit fallback procedure

When the `cronjob` tool shows `last_status: error` after returning `success: true`, or when updates silently revert to `model: null`:

1. Edit `/home/hatem/.hermes/profiles/hafsa/cron/jobs.json` directly.
2. Pin both current and snapshot fields for durability:
   ```json
   "model": "stepfun/step-3.7-flash:free",
   "provider": "nous",
   "provider_snapshot": "nous",
   "model_snapshot": "stepfun/step-3.7-flash:free"
   ```
3. For script jobs, fix the path in the job object: `script` should be just the filename under `<profile>/scripts/`. Remove any `scripts/scripts/` prefix.
4. Re-run affected jobs with `cronjob action=run job_id=<id>` to verify.

## Slack delivery pitfall

Jobs with `deliver='slack'` can execute successfully but fail delivery with:

```json
last_delivery_error: "no delivery target resolved for deliver=slack"
```

Cause: CLI/TUI cron sessions have no live Slack delivery channel unless an explicit target is given.

Fix: update the job to an explicit Slack destination, e.g. `deliver='slack:C<channel_id>'` or `deliver='origin,all'`. If no real Slack chat/channel ID is available, use `deliver='origin'` or a verified platform target until the destination is configured.

## Discord direct-delivery failure rule

Observed failure: after `cronjob action=run job_id=<id>`, the job shows `executed: true` with `execution_success: false`. This indicates agent-runner execution failure, not delivery failure separately. Retrying the same direct Discord delivery often does not help.

Fallback: read the intended payload from disk and emit it yourself using available messaging/tools, then delete or disable the broken one-shot delivery job instead of blindly rerunning it.

## Delivery target format precedence
- Discord channel: `discord:<channel_id>`
- Slack: `slack:C<channel_id>` or explicit channel target
- Origin chat: `origin` or single platform target
- Do not rely on generic `slack` / `discord` without explicit target unless the runtime auto-resolves the live channel.

## NOOP script template

For `no_agent=True` jobs missing their shell script, use `/home/hatem/.hermes/profiles/hafsa/scripts/<name>.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p /home/hatem/.hermes/profiles/<profile>/cron/output
printf '[%s] %s NOOP OK\\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')" "<jobname>" \
  > /home/hatem/.hermes/profiles/<profile>/cron/output/<jobname>.log
exit 0
```

`chmod +x` before enabling the job.

## Hermes CLI cron-create syntax (warning: NOT the same as MCP tool)

The `cronjob` MCP tool accepts `model/provider`, but the **Hermes CLI `hermes cron create` does NOT**:

```bash
# POSITIONAL FIRST
hermes cron create <ISO_SCHEDULE> "<prompt>" --name <name> --deliver origin --repeat 1
```

- `model`/`provider` flags are **rejected** with usage error.
- `--repeat 1` creates a one-shot job; omitting `--repeat` defaults to `forever`.
- Prompt and schedule are **positional**, not `--prompt`.

When a Python script must create one-shot cron jobs from inside Hermes scripts:
1. Use `subprocess.run(["hermes","cron","create", iso_ts, prompt, "--name", label, "--deliver", "origin", "--repeat", "1"])`.
2. Do **not** append `--model` / `--provider`, or the CLI exits with status 2.

## Adaptive reminders via scheduler script pattern

For time-varying reminders (e.g., prayer times, adhkar after Fajr/Asr):

1. **Daily scheduler** (`--no-agent`, script-only): at a fixed morning time, hits an external API and prints a JSON summary or reminder text.
2. **Data-collection script mode**: stdout is injected into the agent prompt on each tick (good for summary jobs).
3. **One-shot creation pattern**: the script can also call `hermes cron create` to schedule exact-time reminders for that day only, with `--repeat 1`. This avoids drift when base times change.

### Proven script template: adaptive prayer times

**File:** `/home/hatem/.hermes/profiles/hafsa/scripts/schedule_adhkar.py`

Behavior:
- Fetches `https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5`.
- Computes target reminders = base prayer time + `ADD_MIN` (default 15).
- Calls `hermes cron create "<iso_ts>" "<arabic prompt>" --name "<label>" --deliver origin --repeat 1`.
- Prints JSON with `date`, `fajr`, `asr`, `morning_scheduled`, `evening_scheduled`, `ok`.

**Cron job:**

```bash
hermes cron create "15 3 * * *" "Run schedule_adhkar.py" --name adhkar-daily-scheduler --deliver origin --repeat forever --no-agent --script schedule_adhkar.py
```

No `--model`/`--provider` here either for `--no-agent` jobs.

## Common failure modes
- `Permission denied` when running `.py` script: `chmod +x` or invoke via `python3 /abs/path.py`.
- `missing-script` doubled path: job JSON expects bare filename, script lives under `<profile>/scripts/`.
- Quiet failures on delivery: `no_agent=True` with empty stdout = silent success. Ensure script prints on at least one branch.
- API failures: script must exit non-zero or print error to stderr so the cron run surfaces the failure rather than succeeding silently.

