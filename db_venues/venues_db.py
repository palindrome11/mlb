import os
import psycopg2
import paths

def upsert_venues_data(venues_data):
    if not venues_data:
        print("dim_venues: nothing to load")
        return
    
    UPSERT_SQL = """
    INSERT INTO dim_venues (
        venue_id,name,city,state,state_abbrev,country,postal_code,latitude,longitude,elevation,
        azimuth_angle,time_zone_id,capacity,turf_type,roof_type,left_line,left_center,center,
        right_center,right_line,active
    )
    VALUES (
       %(venue_id)s,%(name)s,%(city)s,%(state)s,%(state_abbrev)s,%(country)s,%(postal_code)s,%(latitude)s,
       %(longitude)s,%(elevation)s,%(azimuth_angle)s,%(time_zone_id)s,%(capacity)s,%(turf_type)s,%(roof_type)s,
       %(left_line)s,%(left_center)s,%(center)s,%(right_center)s,%(right_line)s,%(active)s
    )
    ON CONFLICT (venue_id) DO UPDATE SET
    name          = EXCLUDED.name,
    city          = EXCLUDED.city,
    state         = EXCLUDED.state,
    state_abbrev  = EXCLUDED.state_abbrev,
    country       = EXCLUDED.country,
    postal_code   = EXCLUDED.postal_code,
    latitude      = EXCLUDED.latitude,
    longitude     = EXCLUDED.longitude,
    elevation     = EXCLUDED.elevation,
    azimuth_angle = EXCLUDED.azimuth_angle,
    time_zone_id  = EXCLUDED.time_zone_id,
    capacity      = EXCLUDED.capacity,
    turf_type     = EXCLUDED.turf_type,
    roof_type     = EXCLUDED.roof_type,
    left_line     = EXCLUDED.left_line,
    left_center   = EXCLUDED.left_center,
    center        = EXCLUDED.center,
    right_center  = EXCLUDED.right_center,
    right_line    = EXCLUDED.right_line,
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
            cur.executemany(UPSERT_SQL, venues_data)
            print(f"dim_venues: {len(venues_data)} venues upserted")
    finally:
        conn.close()



