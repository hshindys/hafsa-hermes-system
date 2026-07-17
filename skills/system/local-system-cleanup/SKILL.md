---
name: local-system-cleanup
description: >
  MUST USE when the user asks for disk cleanup, temp-file purges, cache cleanup,
  disk-usage reporting, or “clean /tmp /var/tmp /home clean” workflows on Linux/Fedora.
  Covers: targeted stale deletion respecting approval gates, npm/pip cache purge,
  podman/Docker caches, disk-usage before/after snapshot, and common permission-denied
  pitfalls on this host.
  NOT for: deleting large unknown trees without scope/boundaries, removing project
  source code from vaults, or mass user-data deletion.
---

# Local System Cleanup

## Trigger phrasing
- “نظف الـ disk”
- “احذف الـ temp files”
- “clean /tmp”
- “disk usage report before/after”
- “clean cache / npm cache / pip cache”

## Prereqs / verified environment
- Fedora 44/Linux workstation
- Zsh/Bash, GNU userland `find`, `du`, `df`, `ncdu` optional
- `npm`, `python3`, `pipx`/`uv` available

## Workflow: audit before delete

1. Take baseline disk-usage snapshot first.
2. Walk suspected-temp roots and print sizes; do not assume totals from `du -sh`.
3. Scope deletion target precisely; do not run recursive sweeps under
   `~/.local/share/containers` or unrelated data folders.

### Baseline snapshot to collect
- `df -h /home/hatem`
- `du -sh /tmp`
- `du -sh "$HOME/.cache"`
- `du -sh "$HOME/.npm"`
- `du -sh "$HOME/tmp"` or equivalent staging temp root used by the user
- `du -sh "$HOME/.local"` — expect permission issues inside container storage

### Temp roots checklist
- `/tmp` own files/dirs only
- `$HOME/tmp` / workspace-specific temp staging
- `$HOME/.cache` shallow stale prune
- `$HOME/.npm`
- `$HOME/.cache/pip`
- `$HOME/.cache/mesa_shader_cache` (low value if stale)

## Paths to avoid for automated deletion
- `$HOME/.local/share/containers/**` — podman/docker storage; permission-denied
  volumes/overlays are expected and must not be mass-deleted
- Any user workspace/docs/downloads/source folders
- `/var/tmp/systemd-private-*` — owned by systemd; skip

## Order of operations

1. Baseline snapshot
2. `/tmp` user-owned stale files
3. `$HOME/tmp` named temp folders older than a safe threshold
4. `$HOME/.cache` shallow prune older than 7 days
5. Tool caches: `npm cache clean --force`, pip cache targets
6. Final snapshot

## Staleness rules (cron-safe defaults)
- `/tmp` user files older than **3 days**
- `$HOME/tmp` / build environments older than **10–14 days**
- `$HOME/.cache` older than **7 days**
- Wenn die Person dann zustimmungsrelevanten Massen- `find` teilt,
  Betrieb nicht blind wiederholen; ruft die Person sodann erneute
  approval-getriebene beratung.

## Hermes approval-gate behavior
On this host, security scoring often turns recursive `find ... -delete` into
[MEDIUM/CRITICAL] approval-gated commands.
- Do not retry the same deletion after timeout.
- Instead, report the blocked scope, files/dir counts, and estimated size.
- Ask/await explicit approval before another bulk delete attempt.
- Preserve blankspace enough to actually speak numbers/estimation
  instead of a giant file list only.

## npm cache cleanup
- Preferred: `npm cache clean --force`
- Fallback nukes caches if `npm` unavailable; but do not remove
  `node_modules/`-owned artifacts accidentally.

## Post-clean verification
- Re-run the baseline snapshot plus:
  - `$HOME/tmp` file count + empty-dir count
  - `.cache` and `.npm` sizes
  - **Safe free-space target for cron jobs:** no free-space guarantee enforced;
    report only if drop significant.
  - Big L—95MB di...

## Reporting format
Present in this exact order:
1. **قبل** — key df/du lines
2. **مفاعيل التنظيف** — which directories were touched
3. **بعد** — key df/du lines
4. **محجوز/محذوف** — before/after delta + what remains
5. If any step was approval-gated, show why cleanup stopped there

## Known pitfalls on this host
- `~/.local/share/containers/storage/volumes/*/_data` read permission denied
- `~/.local/share/containers/storage/tmp` may contain active layers; do not prune blindly
- Flatpak/systemd private dirs in `/var/tmp` are often inaccessible for size reads
- Big `~/.cache` totals can come from browser/Electron package caches; confirm
  impact before broad delete
