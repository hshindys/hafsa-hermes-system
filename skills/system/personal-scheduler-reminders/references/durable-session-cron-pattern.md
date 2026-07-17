# Durable Session Cron Pattern

Use when a cron job must survive crashes/restarts without repeating completed work or losing state.

## Scripts
- `durable-session-hook.sh` <job_id> resume|checkpoint [note]
- `project-verifier.sh` <job_id> [require_checkpoint=1]

## Workflow
1. Job starts with resume: reads last checkpoint from `.../state/durable-session-<job_id>.jsonl`.
2. Agent continues from that state and writes one checkpoint at the end: `checkpoint "<note>"`.
3. For safety jobs, run project-verifier before delivery.

## Example: medication reminder cron
- resume → confirm last delivery day → send today's reminder → checkpoint
- If verifier fails: stop and report; do not auto-send.

## Notes
- State dir: `~/.hermes/profiles/<profile>/scripts/state/`
- Bash or Python crons can use the same hook if invoked via shell.
