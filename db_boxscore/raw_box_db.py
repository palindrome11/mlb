import os,sys
import time
import psycopg2
import json
import paths



def upsert_raw_box_data(cur, game_pk, payload):
    UPSERT_SQL = """
        INSERT INTO boxscore_raw (game_pk, payload, fetched_at)
        VALUES (%s, %s, now())
        ON CONFLICT (game_pk) DO UPDATE
        SET payload = EXCLUDED.payload,
            fetched_at = now()   
        RETURNING (xmax=0) AS inserted 
        """
    cur.execute(UPSERT_SQL, (game_pk, json.dumps(payload)))
    return cur.fetchone()[0]

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    

if __name__ == '__main__':
    main()      
