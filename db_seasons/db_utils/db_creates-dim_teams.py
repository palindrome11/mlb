from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect

def create_seasons():
    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS dim_seasons (
    season                   SMALLINT PRIMARY KEY,
    pre_season_start_date    DATE,
    spring_start_date        DATE,
    spring_end_date          DATE,
    regular_season_start_date DATE,
    last_date_1st_half       DATE,
    all_star_date            DATE,
    first_date_2nd_half      DATE,
    regular_season_end_date  DATE,
    post_season_start_date   DATE,
    post_season_end_date     DATE,
    offseason_start_date     DATE,
    loaded_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    print("dim_seasons table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        create_seasons()
    else:
        print("Run with --create to actually create the table")

if __name__ == '__main__':
    main()      


