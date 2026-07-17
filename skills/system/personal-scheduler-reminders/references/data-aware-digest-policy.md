# Data-Aware Digest Policy

Use this gate whenever an automated digest depends on manager/project reports.

## Gating steps
1. Verify one trusted source end-to-end.
2. Pause digest cron jobs until source is confirmed working.
3. File a submission contract at a fixed repo/vault path with this exact shape:
   - `path`: single stable `.md` path per reporter
   - `deadline`: before Sunday 18:00 Cairo
   - `sections`: status, blockers, asks from management, next-week plan
   - `no-data behavior`: missing report => only report absence; never fabricate or infer
4. Resume digests only after the contract exists and at least one report has been successfully ingested.

## Verification checklist before resume
- [ ] At least one manager report reachable at the contract path
- [ ] Ingestion path works: email via `himalaya`, vault markdown, or verified API
- [ ] Digest job explicitly knows the trusted source path/source in its prompt or workdir
- [ ] Fallback text prepared for when a report arrives late or is empty

## Example paths for this setup
- Source contract: `/home/hatem/Documents/Dina/01-Projects/Directors-Submission-Agreement.md`
- Report target:   `/home/hatem/Documents/Dina/01-Projects/Reports/<project>/weekly-report.md`

## Rule for cron actions
- Partial run is allowed during diagnostics
- A data-dependent cron can stay paused indefinitely until source confirmation ends
- Do not resume based on “we might get data later” optimism