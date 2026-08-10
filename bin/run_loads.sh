#!/usr/bin/env bash
set -euo pipefail
cd /Users/cwconlon/@dev/mlb

echo "--- loading: roster_loads ---"
.venv/bin/python -m basecamp.roster_loads

echo "=== daily roster_loads run finished $(date) ==="
