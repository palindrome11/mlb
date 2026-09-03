from datetime import datetime, date
import os, sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect


def create_date_dim():
    CREATE_SQL = """ 
    CREATE TABLE IF NOT EXISTS dim_date (
        full_date     DATE PRIMARY KEY,
        date_key      INT NOT NULL UNIQUE,     -- 20260812
        year          SMALLINT NOT NULL,
        quarter       SMALLINT NOT NULL,
        month         SMALLINT NOT NULL,
        month_name    TEXT NOT NULL,
        month_abbrev  CHAR(3) NOT NULL,
        day_of_month  SMALLINT NOT NULL,
        day_of_year   SMALLINT NOT NULL,
        day_of_week   SMALLINT NOT NULL,       -- 0=Sunday
        day_name      TEXT NOT NULL,
        day_abbrev    CHAR(3) NOT NULL,
        week_of_year  SMALLINT NOT NULL,
        is_weekend    BOOLEAN NOT NULL,
        is_month_end  BOOLEAN NOT NULL,
        season        SMALLINT,
        season_phase  TEXT,                    -- spring/regular/postseason/offseason
        day_of_season SMALLINT                 -- 1 = opening day
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
    print("dim_dates table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        create_date_dim()
    else:
        print("Run with --create to actually create the date_dim table")

if __name__ == '__main__':
    main()