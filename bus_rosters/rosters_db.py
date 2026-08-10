from datetime import datetime, date
import os, sys
import psycopg2
from dotenv import load_dotenv

def upsert_roster_snapshot_data(roster):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR  = os.path.dirname(BASE_DIR)
   
    loaded = load_dotenv(os.path.join(PROJECT_DIR, '.env'))

    UPSERT_SQL = """
    INSERT INTO roster_snapshots (snapshot_date, team_id, player_id, player_name, position, status) 
    VALUES
        (%(snapshot_date)s, %(team_id)s, %(player_id)s,
        %(player_name)s, %(position)s, %(status)s)
    ON CONFLICT (snapshot_date, team_id, player_id) DO NOTHING;
    """
    
    load_dotenv(os.path.join(BASE_DIR, '.env'))
    
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST','localhost'),
        dbname=os.environ.get('DB_NAME','mlb'),
        user=os.environ.get('DB_USER','postgres'),
        password=os.environ.get('DB_PASSWORD') 
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany(UPSERT_SQL, roster)
                cur.execute("SELECT COUNT(*) FROM roster_snapshots WHERE snapshot_date = %s",
                            (roster[0]['snapshot_date'],))
                print(f"{cur.fetchone()[0]} rows added to roster_snapshots")
        print("roster_snapshot uploaded to database.")
    finally:
        conn.close()
