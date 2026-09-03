from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect

def fact_batting():
    CREATE_SQL = """
    CREATE TABLE fact_batting (
    game_pk        INTEGER NOT NULL REFERENCES dim_games(game_pk),
    player_id      INTEGER NOT NULL REFERENCES dim_players(player_id),
    team_id        INTEGER NOT NULL REFERENCES dim_teams(team_id),
    is_starter     BOOLEAN,
    outs           SMALLINT,        -- store outs, not "innings pitched"
    batters_faced  SMALLINT,
    pitches        SMALLINT,
    strikes        SMALLINT,
    hits           SMALLINT,
    runs           SMALLINT,
    earned_runs    SMALLINT,
    home_runs      SMALLINT,
    walks          SMALLINT,
    intentional_walks SMALLINT,
    strikeouts     SMALLINT,
    hit_batsmen    SMALLINT,
    wild_pitches   SMALLINT,
    balks          SMALLINT,
    inherited_runners SMALLINT,
    inherited_runners_scored SMALLINT,
    decision       CHAR(1),         -- W / L / S / H / NULL
    loaded_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (game_pk, player_id)
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
    print("fact_batting table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        fact_batting()
    else:
        print("Run with --create to actually create the fact_batting table")

if __name__ == '__main__':
    main()      