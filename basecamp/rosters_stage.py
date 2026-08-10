import json
import statsapi
from datetime import datetime, date
import os, sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(BASE_DIR)
ROSTERS_DIR =  os.path.join(PROJECT_DIR,"rosters")
sys.path.insert(0, PROJECT_DIR)

from bus_rosters.rosters_api import capture_roster

selected_teams = [111]

RAW_DATA = os.path.join(PROJECT_DIR, "raw_data", "daily_rosters")
os.makedirs(RAW_DATA, exist_ok=True)

for team_id in selected_teams:
    roster = capture_roster(team_id)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"roster_snapshot_{team_id}_{timestamp}.json"
    fpath = os.path.join(RAW_DATA, fname)
    with open(fpath, 'w') as f:
        json.dump(roster, f, indent=2)
    print(f"Roster snapshot saved to {fpath}")
        
        