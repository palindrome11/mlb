import paths,sys
import argparse
from datetime import date, timedelta

from api_games.games_api import capture_schedule, valid_date
from db_games.games_db import parse_schedule, upsert_games_data

def season_dates(season_year):
    SQL_QUERY = """   
    SELECT 
    regular_season_start_date
    ,regular_season_end_date
    FROM dim_seasons
    WHERE season = 2026
    """ 


def parse_args():
    p = argparse.ArgumentParser(description="Load MLB game schedule into dim_games")
    p.add_argument(
        '--day',
        choices=['today', 'yesterday'],
        default='today',
        help="Which day's games to load (default: today)",
    )
    p.add_argument('--date', help='Specific date, YYYY-MM-DD (overrides --day)')
    p.add_argument(
    '--days-back',
    type=int,
    default=0,
    help='Also reload the N days before the target date (default: 0)',
    )   
    return p.parse_args()

def games_for_date(target_date):
    """Fetch, parse, and load games for a single date."""
    iso = target_date.isoformat()
    print(f"Loading games for {iso}")
    data = capture_schedule(iso, iso)
    game_list = parse_schedule(data)
    print(f"Parsed {len(game_list)} games")
    upsert_games_data(game_list)

def games_for_range(start_date,end_date, game_type='R'):
    print(start_date, end_date)
    start_iso, end_iso = start_date.isoformat(), end_date.isoformat()
    print(f"Loading games for {start_iso} through {end_iso}")
    data = capture_schedule(start_iso, end_iso, game_type=game_type)
    game_list = parse_schedule(data)
    print(f"Parsed {len(game_list)} games")
    print(game_list)
    upsert_games_data(game_list)
   
def main():
    MIN_SEASON = 1876
    #MAX_SEASON = date.today().year + 1
    games_for_range(date(2026, 3, 25), date(2026, 9, 27))
    
 


if __name__ == '__main__':
    sys.exit(main())