# Profile-local HAFSA cron jobs store

Authoritative path: `/home/hatem/.hermes/profiles/hafsa/cron/jobs.json`

Legacy root path: `/home/hatem/.hermes/cron/jobs.json` — often stale; do not edit
unless you are also moving jobs to the profile-local store.

Important: when editing the profile-local file from another profile session,
cross-profile write guard may block writes. Use direct file edit instead of
`cronjob action=update` for `model`/`provider` changes, because that path is
unreliable even when it returns `success: true`.
