from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect


def create_boxscore_raw():
    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS boxscore_raw (
        game_pk  INT PRIMARY KEY,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        payload    JSONB NOT NULL
    )
    """
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
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
        create_boxscore_raw()
    else:
        print("Run with --create to actually create the boxscore_raw table")

if __name__ == '__main__':
    main()      