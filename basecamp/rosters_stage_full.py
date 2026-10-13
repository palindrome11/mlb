import argparse
import json
import os
import sys
from contextlib import closing
from datetime import date, datetime

from api_rosters.rosters_api import capture_roster
from basecamp.db import connect
from bus_teams.teams_u import get_all_teams
from paths import RAW_DATA

ROSTER_TYPES = ["active", "40Man", "fullSeason", "fullRoster", "depthChart"]


def get_team_ids(all_teams: bool, team_ids: list[int] | None) -> list[int]:
    """Every team from the database (--all), or the IDs given on the command line."""
    if all_teams:
        with closing(connect()) as conn:
            return [team["team_id"] for team in get_all_teams(conn)]
    return team_ids


def get_api_output(teams: list[int], roster_type: str, roster_date: date) -> None:
    """Capture each team's roster and write one JSON file per team."""
    for team_id in teams:
        roster = capture_roster(team_id, roster_type=roster_type,
                                roster_date=roster_date.isoformat())
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # Marker for the future when we move all to UTC timestamps
        # tz_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        fname = f"RosterSnapshot_{team_id}_{roster_type}_{roster_date}_{timestamp}.json"
        fpath = RAW_DATA / fname
        with open(fpath, "w") as f:
            json.dump(roster, f, indent=2)
        print(f"Roster snapshot saved to {fpath}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture MLB team rosters and save them to JSON files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  rosters_stage.py --all
  rosters_stage.py --teams 111 147
  rosters_stage.py --all --date 2026-10-01 --roster_type 40Man""",
    )
    who = parser.add_mutually_exclusive_group(required=True)
    who.add_argument("--all", action="store_true", dest="all_teams",
                     help="process every team in the database")
    who.add_argument("--teams", nargs="+", type=int, metavar="TEAM_ID",
                     help="one or more team IDs separated by spaces, e.g. 111 147")
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(),
                        metavar="YYYY-MM-DD",
                        help="roster date (default: today)")
    parser.add_argument("--roster_type", choices=ROSTER_TYPES, default="active",
                        help="roster type to capture (default: active)")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    teams = get_team_ids(args.all_teams, args.teams)
    print(f"Teams ({len(teams)}): {teams}")
    print(f"Roster Type: {args.roster_type}")
    print(f"Roster Date: {args.date}")

    get_api_output(teams, roster_type=args.roster_type, roster_date=args.date)


if __name__ == "__main__":
    main()