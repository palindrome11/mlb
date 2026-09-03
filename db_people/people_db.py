from datetime import datetime, date
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv



def upsert_player_data(players_data):
    
    
    UPSERT_SQL = """
    INSERT INTO dim_players (player_id, full_name, birth_date, birth_country, birth_city, height, bat_side, pitch_hand, 
    primary_position,mlb_debut_date,primary_number,current_age)          
    VALUES
        (%(player_id)s, %(full_name)s, %(birth_date)s, %(birth_country)s, %(birth_city)s, %(height)s,
        %(bat_side)s, %(pitch_hand)s, %(primary_position)s, %(mlb_debut_date)s, %(primary_number)s, %(current_age)s);
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
                cur.executemany(UPSERT_SQL, players_data)
                cur.execute(""" SELECT COUNT(*) FROM dim_players 
                            WHERE loaded_at >= CURRENT_DATE AND 
                            loaded_at <  CURRENT_DATE + 1 """)
                print(f"{cur.fetchone()[0]} rows loaded today:")
                cur.execute("""SELECT full_name FROM dim_players 
                            WHERE loaded_at >= CURRENT_DATE AND 
                            loaded_at <  CURRENT_DATE + 1 """)
                rows = cur.fetchall()
                #print(f"Players")
                for row in rows:
                    print(f"  {row[0]}")
    finally:
        conn.close()

# players_data=[]
# upsert_player_data(players_data)

