import json
import statsapi
from datetime import datetime, date, time
import os, sys
from pathlib import Path
from paths import PROJECT_DIR, RAW_DATA, ARCHIVE_PATH, SQL_DIR, ENV_FILE 
import argparse
from api_rosters.rosters_api import capture_roster_by_date


def validate_date(date_string):
    """Validates the input string matches MM/DD/YYYY and converts it to a date object."""
    try:
        # Tries to parse the string using the specific format
        return datetime.strptime(date_string, "%m/%d/%Y").date()
    except ValueError:
        # Argparse automatically catches ArgumentTypeError and displays a clean error message
        raise argparse.ArgumentTypeError(
            f"'{date_string}' is not a valid date in MM/DD/YYYY format."
        )

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    selected_teams = [111]
    
    parser = argparse.ArgumentParser(
        description="A script that accepts and validates a date."
    )
    
    # Add the date argument with our custom type validator
    parser.add_argument(
        "-d", "--date",
        type=validate_date,
        required=True,
        help="The date to process in MM/DD/YYYY format (e.g., 10/25/2026)"
    )

    args = parser.parse_args() 
    roster_date=args.date
    print(roster_date)
    print(type(roster_date))
    
    if roster_date <= date.today():
        for team_id in selected_teams:
            roster = capture_roster_by_date(team_id, roster_date)
            now = datetime.now()
            roster_dt = datetime.combine(roster_date, time.min)
            if now > roster_dt:
                snapshot_dt = roster_dt.replace(hour=23, minute=59, second=59)
            else:
                snapshot_dt = now
            fname = f"roster_snapshot_{team_id}_{snapshot_dt:%Y%m%d%H%M%S}.json"
            fpath = RAW_DATA / fname
            with open(fpath, 'w') as f:
                json.dump(roster, f, indent=2)
            print(f"Roster snapshot saved to {fpath}")
        
if __name__ == '__main__':
    main()      