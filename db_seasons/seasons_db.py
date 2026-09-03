import os,sys
import psycopg2
import paths

def parse_season(raw):
    #"""Map the API's camelCase payload onto dim_seasons column names."""
    return {
        'season':                    int(raw['seasonId']),
        'pre_season_start_date':     raw.get('preSeasonStartDate'),
        'spring_start_date':         raw.get('springStartDate'),
        'spring_end_date':           raw.get('springEndDate'),
        'regular_season_start_date': raw.get('regularSeasonStartDate'),
        'last_date_1st_half':        raw.get('lastDate1stHalf'),
        'all_star_date':             raw.get('allStarDate'),
        'first_date_2nd_half':       raw.get('firstDate2ndHalf'),
        'regular_season_end_date':   raw.get('regularSeasonEndDate'),
        'post_season_start_date':    raw.get('postSeasonStartDate'),
        'post_season_end_date':      raw.get('postSeasonEndDate'),
        'offseason_start_date':      raw.get('offseasonStartDate'),
    }

def upsert_season_data(season_info):
    UPSERT_SQL = """
    INSERT INTO dim_seasons (
        season, pre_season_start_date, spring_start_date, spring_end_date,
        regular_season_start_date, last_date_1st_half, all_star_date,
        first_date_2nd_half, regular_season_end_date, post_season_start_date,
        post_season_end_date, offseason_start_date
    )
    VALUES (
        %(season)s, %(pre_season_start_date)s, %(spring_start_date)s, %(spring_end_date)s,
        %(regular_season_start_date)s, %(last_date_1st_half)s, %(all_star_date)s,
        %(first_date_2nd_half)s, %(regular_season_end_date)s, %(post_season_start_date)s,
        %(post_season_end_date)s, %(offseason_start_date)s
    )
    ON CONFLICT (season) DO UPDATE SET
        regular_season_start_date = EXCLUDED.regular_season_start_date,
        regular_season_end_date   = EXCLUDED.regular_season_end_date,
        post_season_start_date    = EXCLUDED.post_season_start_date,
        post_season_end_date      = EXCLUDED.post_season_end_date,
        all_star_date             = EXCLUDED.all_star_date,
        loaded_at                 = CURRENT_TIMESTAMP;
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
            cur.executemany(UPSERT_SQL, season_info)
            print(f"dim_seasons: {cur.rowcount} rows affected")
    finally:
        conn.close()

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    

if __name__ == '__main__':
    main()      
