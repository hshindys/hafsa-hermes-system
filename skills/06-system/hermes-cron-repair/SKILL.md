---
name: hermes-cron-repair
description: "Diagnose and fix broken Hermes cron jobs: no_agent script paths, cross-profile cron store, missing scripts, rerun/verify cycle."
version: 1.0.0
author: Hafsa / Hatem
license: MIT
metadata:
  hermes:
    tags: [cron, repair, debugging, scheduler, script-jobs, cross-profile]
    platforms: [linux]
---

# Hermes Cron Repair

MUST USE when: cron jobs are failing, when `cronjob list` shows `last_status: error`, when `no_agent=True` scripts report “Script not found”, or when edits to `/home/hatem/.hermes/cron/jobs.json` block with cross-profile soft-guard errors.

## Trigger phrases
- "fix cron"
- "cron error"
- "Script not found" in cron output
- jobs.json cross-profile blocked
- "crom job"
- "iel el cron"

## Diagnostic checklist

1. **List jobs**
   - Use the Hermes CLI (`hermes cron list`) or expect equivalent structured JSON. Identify every job where `last_status == "error"`.
   - Note agent jobs vs script jobs (`no_agent: true` has a `script` field and no prompt).

2. **Read stored error details**
   - Agent-job clues are often missing from `cronjob list`; inspect `last_error` / `last_delivery_error`.
   - Script-job clues live in:
     - `/home/hatem/.hermes/profiles/<profile>/cron/output/<job_id>/*.md`
     - profile logs at `/home/hatem/.hermes/profiles/<profile>/logs/`

3. **Two canonical failure modes**

   **A. Agent jobs without an effective provider/model**
   - Symptom: `cronjob update ... model=... provider=...` accepted but `cronjob list` still shows `model: null`.
   - Cause: runtime override did not persist / legacy schema mismatch via skill vs cron tool.
   - Workaround: direct edit to `/home/hatem/.hermes/cron/jobs.json` for the failing job IDs with `model` and `provider` fields.

   **B. Script `no_agent=True` path duplication**
   - Symptom: `Script not found: /home/hatem/.hermes/profiles/hafsa/scripts/scripts/<name>.sh`
   - Cause: the configured `script` value is relative and the scheduler prepends `.../scripts/`, so `scripts/...` becomes `.../scripts/scripts/...`.
   - Fix: set `script` to bare file name (`smart-backup.sh`, `auto-tag-watcher.sh`) if the file already lives in the profile `scripts/` dir, or create the missing script there.

4. **Cross-profile cron edits**
   - `/home/hatem/.hermes/cron/jobs.json` is the canonical store now. legacy `~/.hermes/profiles/<profile>/cron/jobs.json` is not read by the scheduler (`#32091`).
   - Editing from another profile triggers soft-guard unless `cross_profile=True` or `write_file`/`patch` is used explicitly for the shared file.

## Repair procedure

### Agent jobs
- Preferred: `cronjob update id=<job_id> model="stepfun/step-3.7-flash:free" provider="nous"`
- Fallback: patch `jobs.json` directly and verify with `cronjob list`.

### Script jobs
- Verify script exists under `/home/hatem/.hermes/profiles/<active_profile>/scripts/`.
- If missing but referenced by skill, create placeholder or disable job.
- If path duplicates: correct `script` field to bare filename.

### Validation
- Re-run the job once (`cronjob run id=...`) and inspect new output under `cron/output/<job_id>/`.
- Re-list jobs and confirm `last_status` flips to `ok`.

## Pitfalls
- The `cronjob` tool sometimes reports back stale/`null` `model` while actually applying the change; trust `jobs.json` and next-run behavior.
- Recurrence `repeat: forever` vs `repeat: 4/100` both exist in this deployment; changing them is harmless but do not unless asked.
- When the only failing jobs are `no_agent=True` and the referenced script is missing, do not spend time changing model/provider; fix script presence/path first.