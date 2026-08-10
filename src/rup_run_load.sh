#!/bin/bash
set -euo pipefail
cd /Users/cwconlon/@dev/mlb && date >> /Users/cwconlon/@dev/mlb/logs/load.log && /Users/cwconlon/@dev/mlb/.venv/bin/python roster_loads.py >> /Users/cwconlon/@dev/mlb/logs/load.log 2>&1