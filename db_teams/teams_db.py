import os
import psycopg2
import paths

def upsert_teams_data(team_data):
    UPSERT_SQL = """
    INSERT INTO dim_teams (
        team_id, name, team_code, abbreviation, club_name, location_name,
        league_id, league_name, division_id, division_name,
        venue_id, venue_name, first_year, active
    )
    VALUES (
        %(team_id)s, %(name)s, %(team_code)s, %(abbreviation)s, %(club_name)s, %(location_name)s,
        %(league_id)s, %(league_name)s, %(division_id)s, %(division_name)s,
        %(venue_id)s, %(venue_name)s, %(first_year)s, %(active)s
    )
    ON CONFLICT (team_id) DO UPDATE SET
        name          = EXCLUDED.name,
        abbreviation  = EXCLUDED.abbreviation,
        league_name   = EXCLUDED.league_name,
        division_name = EXCLUDED.division_name,
        venue_id      = EXCLUDED.venue_id,
        venue_name    = EXCLUDED.venue_name,
        active        = EXCLUDED.active,
        loaded_at     = CURRENT_TIMESTAMP;
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
            cur.executemany(UPSERT_SQL, team_data)
            print(f"dim_teams: {cur.rowcount} rows affected")
    finally:
        conn.close()



