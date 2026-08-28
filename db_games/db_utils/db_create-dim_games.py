from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect

def create_games():
    CREATE_SQL = """ 
    CREATE TABLE IF NOT EXISTS dim_games (
    game_pk          INT PRIMARY KEY,
    official_date    DATE NOT NULL,
    game_datetime    TIMESTAMPTZ,
    season           SMALLINT,
    game_type        CHAR(1),        -- R regular, S spring, P postseason, etc.
    home_team_id     INT REFERENCES dim_teams(team_id),
    away_team_id     INT REFERENCES dim_teams(team_id),
    venue_id         INT,
    game_number      SMALLINT,       -- 1 or 2
    doubleheader     CHAR(1),        -- N, S, Y
    day_night        TEXT,
    coded_game_state CHAR(1),
    resumed_from     DATE,
    rescheduled_from DATE,
    loaded_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
  
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
    )

    try:
        with conn, conn.cursor() as cur:
            cur.execute(CREATE_SQL)
    finally:
        conn.close()
    print("dim_games table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        create_games()
    else:
        print("Run with --create to actually create the games table")

if __name__ == '__main__':
    main()      