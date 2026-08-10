import psycopg2
from dotenv import load_dotenv
import os


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS roster_snapshots (
    snapshot_date  DATE         NOT NULL,
    team_id        INT          NOT NULL,
    player_id      INT          NOT NULL,
    player_name    VARCHAR(100) NOT NULL,
    position       VARCHAR(10),
    status         VARCHAR(50),
    loaded_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (snapshot_date, team_id, player_id)
);
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(BASE_DIR)

loaded = load_dotenv(os.path.join(PROJECT_DIR, '.env'))
#print("BASE_DIR:", BASE_DIR)
#print("PROJECT_DIR:", PROJECT_DIR)
#print(".env found:", loaded)
#print("DB_USER:", os.environ.get('DB_USER'))
#print("DB_PASSWORD set:", os.environ.get('DB_PASSWORD') is not None)
    
conn = psycopg2.connect(
    host=os.environ.get('DB_HOST','localhost'),
    dbname=os.environ.get('DB_NAME','mlb'),
    user=os.environ.get('DB_USER','postgres'),
    password=os.environ.get('DB_PASSWORD') 
)

with conn:
    with conn.cursor() as cur:
        cur.execute(CREATE_SQL)

conn.close()
print("roster_snapshots Table ready.")