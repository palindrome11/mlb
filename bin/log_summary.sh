#!/usr/bin/env bash
set -euo pipefail

LOG="${LOG:-/Users/cwconlon/@dev/mlb/logs/daily.log}"
TARGET="${1:-$(date +%Y-%m-%d)}"
COMPACT=$(date -j -f "%Y-%m-%d" "$TARGET" +%Y%m%d)

echo "=== Summary for $TARGET ==="
grep -E "rows added to roster_snapshots|Archived .*${COMPACT}|run finished" "$LOG" \
  | grep -E "${COMPACT}|rows added"