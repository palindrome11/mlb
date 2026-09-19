#!/bin/bash
set -euo pipefail
cd /Users/cwconlon/@dev/mlb
DAY="${1:-$(date '+%Y-%m-%d')}"
echo "=== $DAY ==="
grep "roster_loads run finished.*$DAY" logs/daily.log | awk '{print $7}' || true
echo "$(grep -c "roster_loads run finished.*$DAY" logs/daily.log || true) load runs of a scheduled 16"
