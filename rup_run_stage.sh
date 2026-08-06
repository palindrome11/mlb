#!/bin/bash
set -euo pipefail
cd /Users/cwconlon/@dev/mlb && date >> /Users/cwconlon/@dev/mlb/logs/capture.log && /Users/cwconlon/@dev/mlb/.venv/bin/python api_get_roster.py >> /Users/cwconlon/@dev/mlb/logs/capture.log 2>&1

