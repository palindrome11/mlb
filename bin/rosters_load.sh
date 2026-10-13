#!/usr/bin/env bash
set -euo pipefail
cd /Users/cwconlon/@dev/mlb

echo "--- loading: game_loads ---"
.venv/bin/python -m basecamp.rosters_load

# echo "=== daily roster_loads run finished $(date) ==="
echo "=== daily roster_loads run finished $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
