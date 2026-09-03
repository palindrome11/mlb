import os,sys
import psycopg2
import paths


def get_missing_venue_ids():
    #"""Venue IDs referenced by games or teams but not yet in dim_venues."""
    QUERY_SQL = """
        SELECT 
        DISTINCT venue_id 
        FROM (
            SELECT venue_id FROM dim_games
            UNION
            SELECT venue_id FROM dim_teams
        ) refs
    WHERE venue_id IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM dim_venues v WHERE v.venue_id = refs.venue_id)  
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
            cur.execute(QUERY_SQL)
            rows = cur.fetchall()
    finally:
        conn.close()

    venue_ids = [row[0] for row in rows]
    print(f"dim_venues: {len(venue_ids)} venue(s) missing")
    return venue_ids


def main():
    venue_ids=get_missing_venue_ids()
    print(venue_ids)

if __name__ == '__main__':
    main()