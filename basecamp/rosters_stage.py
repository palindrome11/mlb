import json
import statsapi
from datetime import datetime, date
import os, sys
from pathlib import Path
from paths import PROJECT_DIR, RAW_DATA, ARCHIVE_PATH, SQL_DIR, ENV_FILE 
from api_rosters.rosters_api import capture_roster


def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    selected_teams = [111]

    for team_id in selected_teams:
        roster = capture_roster(team_id)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        fname = f"roster_snapshot_{team_id}_{timestamp}.json"
        fpath = RAW_DATA / fname
        with open(fpath, 'w') as f:
            json.dump(roster, f, indent=2)
        print(f"Roster snapshot saved to {fpath}")
        
if __name__ == '__main__':
    main()      