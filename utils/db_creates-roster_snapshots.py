import os
import sys

import psycopg2

import paths  # noqa: F401 — imported for its .env loading side effect

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


def create_roster_snapshots():
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
    print("roster_snapshots table ready.")


if __name__ == '__main__':
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    print("uncomment create_roster_snapshots_to_run or exec as module")
    #create_roster_snapshots()