# Nightly Second Brain Compounder

## Purpose
Automate the nightly vault maintenance workflow from the Second Brain video: orphan resolution, mention routing, duplicate merging, MOC updates, and daily summary.

## Where to apply
- `/home/hatem/Documents/Hatem Nad`
- `/home/hatem/Documents/Hafsa`

## Contract
- Input: none (scheduled cron)
- Output: report markdown + vault changes only
- Forbidden: delete files; touch `رواية-كرون/` without explicit permission
- Runs: 23:00 Africa/Cairo daily via cron jobs `1545fe912903` and `64c421fafb51`