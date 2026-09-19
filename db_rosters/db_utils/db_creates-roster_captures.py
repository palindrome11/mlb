import os
import sys

import psycopg2

import paths  # noqa: F401 — imported for its .env loading side effect

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS roster_captures (
    capture_id     bigserial PRIMARY KEY,
    captured_at    timestamptz   NOT NULL DEFAULT now(),
    captured_at_inferred boolean NOT NULL DEFAULT false,
    team_id        INT          NOT NULL REFERENCES dim_teams(team_id),
    roster_type    VARCHAR(100) NOT NULL, 
    source_file    text,       
    player_count   INT          NOT NULL
);

CREATE TABLE roster_capture_members (
    capture_id   bigint NOT NULL REFERENCES roster_captures(capture_id) ON DELETE CASCADE,
    player_id    int NOT NULL,
    player_name  text NOT NULL,
    position     text,
    status       text,
    PRIMARY KEY (capture_id, player_id)
);
"""

def create_roster_captures():
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
    print("roster_captures tables (roster_captures and capture_members) are ready.")


def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    print("This is the capture_rosters  Python module. You must adjust the source code below (uncomment) to exec as a standalone program")
    #create_roster_captures()


if __name__ == '__main__':
    main()