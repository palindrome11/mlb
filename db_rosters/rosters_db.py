from datetime import datetime, date
import os, sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
from paths import PROJECT_DIR, RAW_DATA, ARCHIVE_PATH, SQL_DIR, ENV_FILE 

def upsert_roster_snapshot_data(roster):
    
    UPSERT_SQL = """
    INSERT INTO roster_snapshots (snapshot_date, team_id, player_id, player_name, position, status) 
    VALUES
        (%(snapshot_date)s, %(team_id)s, %(player_id)s,
        %(player_name)s, %(position)s, %(status)s)
    ON CONFLICT (snapshot_date, team_id, player_id) DO NOTHING;
    """
  
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST','localhost'),
        port=os.environ.get('DB_PORT', 5432),
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
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
