# Cron Drift & Script Path Fixes

## Error Signature 1: Global Inference Config Drift

**When it happens**
After changing Hermes global provider/model (e.g., `nous -> openrouter`, or model rename), any previously created unpinned agent cron job fails at runtime.

**Exact message**
```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'nous' -> 'openrouter'; model 'stepfun/step-3.7-flash:free' -> 'openrouter/google/gemma-4-31b-it:free'), and this job is unpinned. No inference call was made. To run on the new config, pin it explicitly: `cronjob action=update job_id=<id> provider=<provider> model=<model>` (or pin the original values to keep them). See #44585.
```

**Recovery**
```
cronjob action=update job_id=<id> provider=nous model=stepfun/step-3.7-flash:free
cronjob action=run job_id=<id>
```

**Affected jobs in this session**
- `1573274fddf9` Weekly Directors Digest
- `c9cfb680d218` GitHub Triage Alert — Daily
- `a1441833b962` World Cup 2026 table update daily 08:00 Cairo
- `573d2ac7e79f` World Cup Egypt — Daily Brief
- `1ca0b3397d11` Dina Projects Daily Brief

**Prevention**
Always pin provider/model explicitly on `cronjob action='create'`, never rely on inherited defaults.

---

## Error Signature 2: Script Not Found / Nested scripts/scripts Path

**When it happens**
A `no_agent=True` cron job points to a script path that is either absolute/home-relative or nests under a `scripts/` prefix when only a filename is expected.

**Exact message**
```
Script not found: /home/hatem/.hermes/profiles/hafsa/scripts/scripts/smart-backup.sh
```
or with update:
```
Script path must be relative to ~/.hermes/scripts/. Got absolute or home-relative path: '/home/hatem/.hermes/profiles/hafsa/scripts/smart-backup.sh'. Place scripts in ~/.hermes/scripts/ and use just the filename.
```

**Recovery**
```bash
mkdir -p ~/.hermes/scripts
cp -f <source-script-path> ~/.hermes/scripts/<name>.sh
chmod +x ~/.hermes/scripts/<name>.sh
```
Then:
```
cronjob action=update job_id=<id> script=<name>.sh
```

**Affected jobs in this session**
- `89c404d8b200` Daily Smart Vault Backup
- `413677ae0c7f` Auto-Tagging Watcher

**Prevention**
Register all cron script paths as bare filenames that exist under `~/.hermes/scripts/`. Never use profile-local script paths for cron jobs.

---

## Error Signature 3: HTTP 401 User not found in agent-mode cron

**When it happens**
An agent-mode cron fails with auth/session error even though other jobs succeed.

**Exact message seen**
```
RuntimeError: HTTP 401: User not found.
```

**Recovery**
Verify auth state, then run the job once manually:
```
cronjob action=run job_id=<id>
```
If it succeeds on manual rerun, the failure was transient session/auth state, not prompt content.

**Affected jobs in this session**
- `66141ac500f3` Weekly Disk Cleanup — succeeded on manual rerun after initial 401
