from __future__ import annotations
 
import sys, os 
 
from datetime import date, datetime
from contextlib import closing
from pathlib import Path
from typing import Any
 
from psycopg2.extras import RealDictCursor, execute_values
 
from basecamp.db import connect

import argparse


def set_game_date(user_date: str) -> date:
    return date.fromisoformat(user_date)

def get_game_team_ids(game_date: date, conn: Any) -> list[(int, int)]:
    """Team IDs present in dim_games as home and away teams."""
    RETRIEVE_SQL = """
    SELECT
    home_team_id
    ,away_team_id
    FROM dim_games g
    JOIN dim_venues v 
    ON g.venue_id = v.venue_id
    WHERE official_date = %(game_date)s;
    """
    with conn.cursor() as cur:
        cur.execute(RETRIEVE_SQL, {'game_date': game_date})
        return [(row[0], row[1]) for row in cur.fetchall()]


def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    parser = argparse.ArgumentParser(description="Specify the date for game team ID retrieval.")
    parser.add_argument('--date', type=str, help='Date for game team ID retrieval in YYYY-MM-DD format')
     
    args = parser.parse_args()
    games_date = args.date #if args.date else date.today().isoformat()

    if games_date:
        print(f"Games Date: {games_date}")
        #game_date=set_game_date('2026-10-08')
        conn = connect()
        teams = get_game_team_ids(games_date, conn)
        print(teams)
    else:
        print("No games date specified. Specify a date using the --date flag using YYYY-MM-DD format.")

if __name__ == '__main__':
    main()      

