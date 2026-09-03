import paths,sys
import argparse
from datetime import date

from api_seasons.season_api import get_season_info
from db_seasons.seasons_db import upsert_season_data , parse_season

def main():
    MIN_SEASON = 1876

    p = argparse.ArgumentParser(description="Load MLB season date info")
    p.add_argument('--season', type=int, help='Season year (YYYY)')
    args = p.parse_args()

    max_season = date.today().year + 1
    season_year = args.season

    if season_year is None:
        try:
            season_year = int(input(f"Enter MLB season year ({MIN_SEASON}-{max_season}): "))
        except ValueError:
            print("Not a valid year.")
            return(1)

    if not MIN_SEASON <= season_year <= max_season:
        print(f"Year must be between {MIN_SEASON} and {max_season}")
        return 1

    raw_seasons = get_season_info(season_year)
    print(raw_seasons)
    season_rows = [parse_season(s) for s in raw_seasons]
    print(season_rows)
    upsert_season_data(season_rows)


if __name__ == '__main__':
    sys.exit(main())