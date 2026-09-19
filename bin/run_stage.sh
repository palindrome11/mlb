#!/usr/bin/env bash
set -euo pipefail
cd /Users/cwconlon/@dev/mlb

echo "--- staging: rosters_stage ---"
.venv/bin/python -m basecamp.rosters_stage

# echo "=== daily rosters_stage run finished $(date) ==="
echo "=== daily rosters_stage run finished $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
