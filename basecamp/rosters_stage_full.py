import json
import statsapi
from datetime import datetime, date, timezone
import os, sys
from pathlib import Path
from paths import PROJECT_DIR, RAW_DATA, ARCHIVE_PATH, SQL_DIR, ENV_FILE 
from api_rosters.rosters_api import capture_roster
import argparse

def get_team_ids(team_ids=111):
    teams=[team_ids]# Example function to retrieve team IDs; replace with actual logic as needed
    return teams  # Replace with actual team IDs    
def get_api_output(teams, roster_type='active', roster_date=date.today().isoformat()):
    for team_id in teams:
            roster = capture_roster(team_id,roster_type=roster_type, roster_date=roster_date)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            ##Marker for the future when we move all to UTC timestamps
            #tz_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            fname = f"SpecializedRosterSnapshot_{team_id}_{roster_type}_{roster_date}_{timestamp}.json"
            fpath = RAW_DATA / fname
            with open(fpath, 'w') as f:
                json.dump(roster, f, indent=2)
            print(f"Roster snapshot saved to {fpath}")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    parser = argparse.ArgumentParser(description="Capture MLB team rosters and save to JSON files. Optionally specify team IDs, roster type, and date.")
    parser.add_argument('--teams', nargs='+', type=str, help='List of team IDs to process sepated by space. If not provided, only the Red Sox will be processed.')
    parser.add_argument('--date', type=str, help='Date for roster capture in YYYY-MM-DD format')
    parser.add_argument('--roster_type', type=str, default='active', help='Type of roster to capture (Active,40Man,fullSeason Default:active')  
    
    args = parser.parse_args()
    teams = args.teams if args.teams else get_team_ids()
    print(teams)
    roster_date = args.date if args.date else date.today().isoformat()
    roster_type = args.roster_type if args.roster_type else 'active'
        
    print(f"Teams: {teams}")
    print(f"Roster Type: {roster_type}")
    print(f"Roster Date: {roster_date}")
    
    get_api_output(teams, roster_type=roster_type, roster_date=roster_date)
       
        
if __name__ == '__main__':
    main()      