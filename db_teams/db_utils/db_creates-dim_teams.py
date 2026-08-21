from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect

def create_dim_teams():
    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS dim_teams (
        team_id             INT PRIMARY KEY,
        name                TEXT NOT NULL,
        team_code           TEXT,
        abbreviation        TEXT,
        club_name           TEXT,
        location_name       TEXT,
        league_id           INT,
        league_name         TEXT,
        division_id         INT,
        division_name       TEXT,
        venue_id            INT,
        venue_name          TEXT,
        first_year          TEXT,
        active              BOOLEAN,
        loaded_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
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
    print("dim_teams table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        create_dim_teams()
    else:
        print("Run with --create to actually create the table")

if __name__ == '__main__':
    main()      


