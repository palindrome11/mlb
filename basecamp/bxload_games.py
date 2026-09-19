import os, sys
# from certifi.__main__ import args
# from dotenv import parser
import psycopg2
import time
import paths

import argparse

from api_boxscore.boxscore_api import capture_boxscore
from db_boxscore.raw_box_db import upsert_raw_box_data

FETCH_DELAY = 1.0

def comma_separated_integers(value):
    return [int(item) for item in value.split(',')]

def get_connection():
    return psycopg2.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    port=int(os.environ.get('DB_PORT', 5432)),
    dbname=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    )

def get_games_missing_boxscores(cur):
    MISSING_BOXSCORES_SQL = """
    SELECT g.game_pk
    FROM dim_games g
    LEFT JOIN boxscore_raw b ON b.game_pk = g.game_pk
    WHERE b.game_pk IS NULL
    AND coded_game_state = 'F'  
    ORDER BY g.game_pk 
    """
    cur.execute(MISSING_BOXSCORES_SQL)
    return [row[0] for row in cur.fetchall()]

#def fetch_boxscore(game_pk):
#    """Pull the raw boxscore payload for one game."""
#   return statsapi.get('game_boxscore', {'gamePk': game_pk})

#def stage_raw_box_data(cur, game_pk, payload):
#    """Insert or refresh one boxscore payload. Returns True if newly inserted."""
#    cur.execute(UPSERT_SQL, (game_pk, Json(payload)))
#    return cur.fetchone()[0]

def main():
      
    parser = argparse.ArgumentParser(description="Process a group of game ids.")
    parser.add_argument(
        '--game_ids', 
        type=comma_separated_integers, 
        required=True,
        help='Comma-separated numbers (e.g., 1,2,3,4)'
    )

    args = parser.parse_args()
    print("Parsed list:", args.game_ids)
    explicit_pks=args.game_ids
    total_games_needing_boxcores = len(explicit_pks)
           
    conn = get_connection()
    inserted = refreshed = failed = 0
    
    
    try:
        with conn.cursor() as cur:
            for i , game_pk in enumerate(explicit_pks):
                if i:
                    time.sleep(FETCH_DELAY)
                try:
                    payload = capture_boxscore(game_pk)
                    was_insert = upsert_raw_box_data(cur, game_pk, payload)
                    remaining_games_to_process = total_games_needing_boxcores - i
                    print(f"Game Number {game_pk} processing with {remaining_games_to_process} remaining to process")
                    conn.commit()
                except Exception as exc:
                    conn.rollback() 
                    failed += 1
                    print(f"  {game_pk}: FAILED ({exc})", file=sys.stderr)
                    continue   
                if was_insert:
                    inserted += 1
                else:     
                    refreshed += 1
    finally: 
        conn.close()
    
    print(f"boxscore_raw: {inserted} staged, {refreshed} refreshed, {failed} failed")
    return 1 if failed else 0

if __name__ == '__main__':        
    main()
