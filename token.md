# ⚠️ GitHub PAT Token — REVOKED & REDACTED

> WARNING: The original token stored here was a live GitHub Personal Access Token in
> plaintext. Plaintext credentials inside a synced vault (OneDrive / Drive) are a leak
> risk and were exposed. **Treat the old token as compromised.**

## Action required — rotate immediately
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Find the token (classic `glpat-…`, prefix `…01.171m63p3n`) and **Revoke** it.
3. Generate a new PAT only if still needed, with the minimum scopes required.
4. Store it in a secret manager or Hermes credential store — **never** in a synced vault file.

## Old token (DO NOT USE — revoked)
```
«REDACTED — revoked on 2026-08-06»
```

## Safe usage going forward
- Prefer GitHub CLI auth (`gh auth login`) over a stored PAT.
- If a token is unavoidable, keep it in an environment variable or OS keychain,
  outside any cloud-synced folder.

*Redacted by Hermes agent on 2026-08-06.*
