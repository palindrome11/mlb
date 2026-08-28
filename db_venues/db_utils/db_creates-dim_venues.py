from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect

def create_dim_venues():
    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS dim_venues (
        venue_id      INT PRIMARY KEY,
        name          TEXT NOT NULL,
        city          TEXT,
        state         TEXT,
        state_abbrev  CHAR(2),
        country       TEXT,
        postal_code   TEXT,
        latitude      NUMERIC(10,7),
        longitude     NUMERIC(10,7),
        elevation     INT,
        azimuth_angle NUMERIC(5,2),
        time_zone_id  TEXT,
        capacity      INT,
        turf_type     TEXT,
        roof_type     TEXT,
        left_line     INT,
        left_center   INT,
        center        INT,
        right_center  INT,
        right_line    INT,
        active        BOOLEAN,
        loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    print("dim_venues table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        create_dim_venues()
    else:
        print("Run with --create to actually create the table")

if __name__ == '__main__':
    main()      


