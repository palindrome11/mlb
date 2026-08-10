#!/usr/bin/env bash
set -euo pipefail

LOG="${LOG:-/Users/cwconlon/@dev/mlb/logs/daily.log}"
TARGET="${1:-$(date +%Y-%m-%d)}"

COMPACT=$(date -j -f "%Y-%m-%d" "$TARGET" +%Y%m%d)
HUMAN=$(date -j -f "%Y-%m-%d" "$TARGET" "+%a %b %e")

echo "=== Runs for $TARGET ==="

awk -v c="$COMPACT" -v h="$HUMAN" '
  /^--- staging:/ { block = "" }
                  { block = block $0 ORS }
  /^=== daily roster_loads run finished/ {
      if (block ~ c || block ~ h) printf "%s", block
      block = ""
  }
' "$LOG"