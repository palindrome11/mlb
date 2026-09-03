import os
import sys

import psycopg2

import paths  # noqa: F401 — imported for its .env loading side effect

ALTER_SQL = """
ALTER TABLE roster_snapshots
    ADD COLUMN version    integer     NOT NULL DEFAULT 1,
    ADD COLUMN updated_at timestamptz NOT NULL DEFAULT now()
"""

def alter_roster_snapshots():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
    )
    try:
        with conn, conn.cursor() as cur:
            cur.execute(ALTER_SQL)
    finally:
        conn.close()
    print("roster_snapshots table structure updated.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')})")
    print("This is the alter_roster_snapshots Python module. You must adjust the source code to exec as a standalone program")
    #alter_roster_snapshots()


if __name__ == '__main__':
    main()