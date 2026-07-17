#!/usr/bin/env bash
# local-system-cleanup verify script
set -euo pipefail
hdf="${1:-/home/hatem}"
echo "=== disk baseline ==="
df -h "$hdf" || true
echo "=== temp/cache sizes ==="
du -sh "$hdf/tmp" 2>/dev/null || true
du -sh "$hdf/.cache" 2>/dev/null || true
du -sh "$hdf/.npm" 2>/dev/null || true
du -sh "$hdf/.local" 2>/dev/null || true
du -sh /tmp 2>/dev/null || true
