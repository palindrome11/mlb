from html import parser
from unittest import result

from requests.packages import target

from basecamp.dim_venues_build import add_individual_venues
import paths,sys
import argparse
from datetime import date, timedelta

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from api_games.games_api import capture_schedule, valid_date
from db_games.games_db import parse_schedule, upsert_games_data

from basecamp.game_spec import PHASE_TO_TYPES, RequestSpec, expand
from basecamp.games_stage import stage_all
from basecamp.games_loads import load_files

def games_for_date(target_date):
    """Fetch, parse, and load games for a single date."""
    iso = target_date.isoformat()
    print(f"Loading games for {iso}")
    data = capture_schedule(iso, iso)
    game_list = parse_schedule(data)
    print(f"Parsed {len(game_list)} games")
    upsert_games_data(game_list)

def games_for_range(start_date,end_date):
    start_iso, end_iso = start_date.isoformat(), end_date.isoformat()
    print(f"Loading games for {start_iso} through {end_iso}")
    data = capture_schedule(start_iso, end_iso)
    game_list = parse_schedule(data)
    print(f"Parsed {len(game_list)} games")
    upsert_games_data(game_list)
   
def main():
    MIN_SEASON = 1876
    #MAX_SEASON = date.today().year + 1

    parser = argparse.ArgumentParser(
    description="Add game information to the database by date or date range."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--date", nargs="+", type=date.fromisoformat, metavar="YYYY-MM-DD",
         help="One or more individual dates",
    )
    target.add_argument(
        "--date_range", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
        help="Inclusive start and end date",
    )
    parser.add_argument(
        "--phase",
        nargs="+",
        choices=sorted(PHASE_TO_TYPES),
        default=["regular"],
        help="Game types to load (default: regular)",
    )   
    parser.add_argument(
    "--dry_run",
    action="store_true",
    help="Print the windows that would be fetched, then exit without calling the API",
    )
    args = parser.parse_args()

    if args.date:
        specs = [RequestSpec(mode="range", start_date=d, end_date=d, phases=args.phase) for d in args.date]
    else:
        start, end = args.date_range
        specs = [RequestSpec(mode="range", start_date=start, end_date=end, phases=args.phase)]

   # for spec in specs:
   #     load_files([p for p, _ in stage_all(expand(spec))], conn_info=conn_info)
    for spec in specs:
        windows = expand(spec, None)
        if args.dry_run:
            for w in windows:
                print(f"{w.label}  types={','.join(w.game_types)}  days={w.days}")
            print(f"{len(windows)} request(s), {sum(w.days for w in windows)} days")
            continue
        staged = [p for p, _ in stage_all(windows)]
        print(staged)
        #exit()
        result = load_files(staged)
        print(f"{result['rows']} rows, {result['duplicates']} duplicates collapsed")

       


if __name__ == '__main__':
   main()