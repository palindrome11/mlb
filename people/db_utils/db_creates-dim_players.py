from datetime import datetime, date
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

def project_root(marker='.git'):
    for parent in Path(__file__).resolve().parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"No {marker} found above {__file__}")

PROJECT_DIR = project_root()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#PROJECT_DIR  = os.path.dirname(BASE_DIR)
print(f"PROJECT DIRECTORY {PROJECT_DIR}")

#load_dotenv(os.path.join(PROJECT_DIR, '.env'))

loaded = load_dotenv(os.path.join(PROJECT_DIR, '.env'))
#print("BASE_DIR:", BASE_DIR)
#print("PROJECT_DIR:", PROJECT_DIR)
#print(".env found:", loaded)
#print("DB_USER:", os.environ.get('DB_USER'))
#print("DB_PASSWORD set:", os.environ.get('DB_PASSWORD') is not None)
  
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS dim_players (
    player_id       INT PRIMARY KEY,
    full_name       TEXT NOT NULL,
    birth_date      DATE,
    birth_country   TEXT,
    birth_city      TEXT,
    height          TEXT,
    bat_side        CHAR(1),
    pitch_hand      CHAR(1),
    primary_position TEXT,
    mlb_debut_date  DATE,
    primary_number   INT,
    current_age      INT,
    loaded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
   
conn = psycopg2.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    port=os.environ.get('DB_PORT', 5432),
    dbname=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
)

with conn:
    with conn.cursor() as cur:
        cur.execute(CREATE_SQL)

conn.close()
print("dim_players Table ready.")


