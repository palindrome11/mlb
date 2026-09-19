from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect

def fact_pitching():
    CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS fact_pitching (
    game_pk                  integer NOT NULL REFERENCES dim_games(game_pk),
    player_id                integer NOT NULL,
    team_id                  integer NOT NULL REFERENCES dim_teams(team_id),
    is_starter               boolean NOT NULL DEFAULT false,
    outs_recorded            smallint NOT NULL DEFAULT 0,  -- 19 = 6.1 IP
    batters_faced            smallint NOT NULL DEFAULT 0,
    hits                     smallint NOT NULL DEFAULT 0,
    runs                     smallint NOT NULL DEFAULT 0,
    earned_runs              smallint NOT NULL DEFAULT 0,
    home_runs                smallint NOT NULL DEFAULT 0,
    walks                    smallint NOT NULL DEFAULT 0,
    intentional_walks        smallint NOT NULL DEFAULT 0,
    hit_batsmen              smallint NOT NULL DEFAULT 0,
    strikeouts               smallint NOT NULL DEFAULT 0,
    wild_pitches             smallint NOT NULL DEFAULT 0,
    balks                    smallint NOT NULL DEFAULT 0,
    pitches_thrown           smallint NOT NULL DEFAULT 0,
    strikes                  smallint NOT NULL DEFAULT 0,
    inherited_runners        smallint NOT NULL DEFAULT 0,
    inherited_runners_scored smallint NOT NULL DEFAULT 0,
    is_win                   boolean NOT NULL DEFAULT false,
    is_loss                  boolean NOT NULL DEFAULT false,
    is_save                  boolean NOT NULL DEFAULT false,
    holds                    smallint NOT NULL DEFAULT 0,
    blown_saves              smallint NOT NULL DEFAULT 0,
    loaded_at                timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (game_pk, player_id)
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
    print("fact_pitching table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        fact_pitching()
    else:
        print("Run with --create to actually create the fact_pitching table")

if __name__ == '__main__':
    main()      