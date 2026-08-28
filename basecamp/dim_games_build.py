import paths,sys
import argparse
from datetime import date, timedelta

from api_games.games_api import capture_schedule, valid_date
from db_games.games_db import parse_schedule, upsert_games_data

def parse_args():
    p = argparse.ArgumentParser(description="Load MLB game schedule into dim_games")
    p.add_argument(
        '--day',
        choices=['today', 'yesterday'],
        default='today',
        help="Which day's games to load (default: today)",
    )
    p.add_argument('--date', help='Specific date, YYYY-MM-DD (overrides --day)')
    return p.parse_args()

def games_for_date(target_date):
    """Fetch, parse, and load games for a single date."""
    iso = target_date.isoformat()
    print(f"Loading games for {iso}")
    data = capture_schedule(iso, iso)
    game_list = parse_schedule(data)
    print(f"Parsed {len(game_list)} games")
    upsert_games_data(game_list)
   
def main():
    MIN_SEASON = 1876
    #MAX_SEASON = date.today().year + 1
 
    args = parse_args()

    if args.date:
        target = date.fromisoformat(args.date)
    elif args.day == 'yesterday':
        target = date.today() - timedelta(days=1)
    else:
        target = date.today()

    games_for_date(target)
    return 0
 
#   p = argparse.ArgumentParser(description="Load game data")
#  p.add_argument('--season', type=int, help='Season year (YYYY)')
#    args = p.parse_args()
#
#  
#    season_year = args.season
#
#    if season_year is None:
#        try:
#            season_year = int(input(f"Enter MLB season year ({MIN_SEASON}-{max_season}): "))
#        except ValueError:
#            print("Not a valid year.")
#            return(1)
#
#    if not MIN_SEASON <= season_year <= max_season:
#        print(f"Year must be between {MIN_SEASON} and {max_season}")
#        return 1
#
#    raw_seasons = get_season_info(season_year)
#    print(raw_seasons)
#    season_rows = [parse_season(s) for s in raw_seasons]
#    print(season_rows)
#    upsert_season_data(season_rows)


if __name__ == '__main__':
    sys.exit(main())