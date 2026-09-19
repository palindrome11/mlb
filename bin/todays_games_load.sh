#!/usr/bin/env bash
set -euo pipefail
cd /Users/cwconlon/@dev/mlb

RUN_DATE="${1:-$(date +%Y-%m-%d)}"
STAMP_FMT='+%Y-%m-%d %H:%M:%S %Z'

trap 'echo "=== game_loads FAILED for $RUN_DATE at $(date "$STAMP_FMT") ==="' ERR

echo "--- loading: games_load for $RUN_DATE ---"
.venv/bin/python -m basecamp.dim_games_build --date "$RUN_DATE"

echo "=== daily game_loads run finished $RUN_DATE at $(date "$STAMP_FMT") ==="
