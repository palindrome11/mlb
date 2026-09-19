from datetime import datetime, date
import os,sys
import psycopg2
import paths  # noqa: F401 — imported for its .env loading side effect

def fact_batting():
    CREATE_SQL = """
    CREATE TABLE fact_batting (
    game_pk             integer NOT NULL REFERENCES dim_games(game_pk),
    player_id           integer NOT NULL,
    team_id             integer NOT NULL REFERENCES dim_teams(team_id),
    batting_order       smallint,          -- 1-9, NULL if never batted
    batting_sub_index   smallint,          -- 0 = original occupant of the slot
    position            text,
    plate_appearances   smallint NOT NULL DEFAULT 0,
    at_bats             smallint NOT NULL DEFAULT 0,
    runs                smallint NOT NULL DEFAULT 0,
    hits                smallint NOT NULL DEFAULT 0,
    doubles             smallint NOT NULL DEFAULT 0,
    triples             smallint NOT NULL DEFAULT 0,
    home_runs           smallint NOT NULL DEFAULT 0,
    rbi                 smallint NOT NULL DEFAULT 0,
    walks               smallint NOT NULL DEFAULT 0,
    intentional_walks   smallint NOT NULL DEFAULT 0,
    hit_by_pitch        smallint NOT NULL DEFAULT 0,
    strikeouts          smallint NOT NULL DEFAULT 0,
    sac_bunts           smallint NOT NULL DEFAULT 0,
    sac_flies           smallint NOT NULL DEFAULT 0,
    stolen_bases        smallint NOT NULL DEFAULT 0,
    caught_stealing     smallint NOT NULL DEFAULT 0,
    gidp                smallint NOT NULL DEFAULT 0,
    left_on_base        smallint NOT NULL DEFAULT 0,
    total_bases         smallint NOT NULL DEFAULT 0,
    loaded_at           timestamptz NOT NULL DEFAULT now(),
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