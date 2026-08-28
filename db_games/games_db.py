import os,sys
import psycopg2
import paths

def parse_schedule(data):
    # """Flatten the nested schedule payload into flat dicts for dim_games."""
    rows = []
    for day in data.get('dates', []):
        for g in day.get('games', []):
            rows.append({
                'game_pk':          g['gamePk'],
                'official_date':    g.get('officialDate'),
                'game_datetime':    g.get('gameDate'),
                'season':           int(g['season']) if g.get('season') else None,
                'game_type':        g.get('gameType'),
                'home_team_id':    (g.get('teams', {}).get('home', {}).get('team') or {}).get('id'),
                'away_team_id':    (g.get('teams', {}).get('away', {}).get('team') or {}).get('id'),
                'venue_id':        (g.get('venue') or {}).get('id'),
                'game_number':      g.get('gameNumber'),
                'doubleheader':     g.get('doubleHeader'),
                'day_night':        g.get('dayNight'),
                'coded_game_state': g.get('status', {}).get('codedGameState'),
                'resumed_from':     g.get('resumedFrom'),
                'rescheduled_from': g.get('rescheduledFrom'),
            })
    return rows


def upsert_games_data(game_list):
    UPSERT_SQL = """
    INSERT INTO dim_games (
        game_pk, official_date, game_datetime, season, game_type, home_team_id, away_team_id, 
        venue_id, game_number, doubleheader, day_night, coded_game_state, resumed_from, rescheduled_from
    )
    VALUES (
            %(game_pk)s, %(official_date)s, %(game_datetime)s, %(season)s, %(game_type)s, %(home_team_id)s, 
            %(away_team_id)s, %(venue_id)s, %(game_number)s, %(doubleheader)s, 
            %(day_night)s, %(coded_game_state)s, %(resumed_from)s, %(rescheduled_from)s       
    )
    ON CONFLICT (game_pk) -- Properly targets the unique game ID
    DO UPDATE SET 
        coded_game_state = EXCLUDED.coded_game_state,
        resumed_from = EXCLUDED.resumed_from,
        rescheduled_from = EXCLUDED.rescheduled_from,
        loaded_at = CURRENT_TIMESTAMP;
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
            cur.executemany(UPSERT_SQL, game_list)
            print(f"dim_seasons: {cur.rowcount} rows affected")
    finally:
        conn.close()

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    

if __name__ == '__main__':
    main()      
