"""
## Run this as a stremlit app in a browser as seen in the below cli command:
##           .venv/bin/streamlit run ./basecamp/sl_gameclock.py
##
"""
import streamlit as st

from contextlib import closing

import pandas as pd
from psycopg2.extras import RealDictCursor

from basecamp.db import connect

def run_query(sql: str, params: tuple | dict | None = None) -> pd.DataFrame:
    """Run a SELECT and return the rows as a DataFrame."""
    with closing(connect()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return pd.DataFrame(cur.fetchall())

@st.fragment(run_every="60s")
def game_clock():
  df = run_query("""
  WITH early_to_late_games AS 
  (
  SELECT
   g.game_pk AS game_pk
  ,CONCAT(wt.name, ' (', wt.team_id, ')') AS away_team
  ,CONCAT(ht.name, ' (', ht.team_id, ')') AS home_team 
  ,v.name AS venue
  ,g.official_date AS game_date
  ,g.game_datetime 
  ,v.time_zone_id
  ,to_char(g.game_datetime AT TIME ZONE v.time_zone_id, 'FMHH12:MI AM') AS venue_start_time
  ,v.time_zone_id AS venue_timezone
  ,to_char(ROUND(EXTRACT(EPOCH FROM (g.game_datetime - now()) / 3600),2) * interval ' 1 hour', 'FMHH24" hrs "FMMI" min"')  AS hours_to_game
  ,CONCAT(v.city, ',', v.state, NULL) AS venue_location
  ,game_type AS game_type
  ,row_number() OVER (ORDER BY g.game_datetime) AS early_to_late
  FROM dim_games g
  JOIN dim_teams ht ON ht.team_id = g.home_team_id
  JOIN dim_teams wt ON wt.team_id = g.away_team_id
  JOIN dim_venues v ON v.venue_id = g.venue_id
  WHERE official_date = current_date 
 ),
 client AS (
    SELECT local_tz
    FROM client_config
  )
  SELECT 
  game_pk
  ,CASE 
    WHEN game_type = 'S' THEN 'Spring Training'
    WHEN game_type = 'R' THEN 'Regular Season'
    WHEN game_type = 'F' THEN 'Wild Card'
    WHEN game_type = 'D' THEN 'Division Series'
    WHEN game_type = 'L' THEN 'League Championship Series' 
    WHEN game_type = 'W' THEN 'World Series'
    WHEN game_type = 'C' THEN 'Championship'
    WHEN game_type = 'P' THEN 'Postseason'
    WHEN game_type = 'A' THEN 'All-Star Game'
    WHEN game_type = 'I' THEN 'Intrasquad'
    WHEN game_type = 'E' THEN 'Exhibition'
   END AS game_type
  ,game_date
  ,away_team
  ,home_team
  ,venue
  ,venue_location
  ,venue_timezone
  ,venue_start_time
  ,to_char(now() AT TIME ZONE venue_timezone,'FMHH12:MI AM') AS current_venue_time 
  ,hours_to_game
  ,c.local_tz
  ,to_char(now() AT TIME ZONE c.local_tz,'FMHH12:MI AM') AS current_local_time
  ,to_char(g.game_datetime AT TIME ZONE c.local_tz, 'FMHH12:MI AM') AS local_start_time
  ,CASE WHEN ROUND(EXTRACT(EPOCH FROM ((now() AT TIME ZONE c.local_tz) - (now() AT TIME ZONE venue_timezone))) / 3600) > 0 THEN '+'
     WHEN ROUND(EXTRACT(EPOCH FROM ((now() AT TIME ZONE c.local_tz) - (now() AT TIME ZONE venue_timezone))) / 3600) < 0 THEN ''
     ELSE ' ' END
  || ROUND(EXTRACT(EPOCH FROM ((now() AT TIME ZONE c.local_tz) - (now() AT TIME ZONE venue_timezone))) / 3600)::int
  || CASE WHEN ABS(ROUND(EXTRACT(EPOCH FROM ((now() AT TIME ZONE c.local_tz) - (now() AT TIME ZONE venue_timezone))) / 3600)) = 1
         THEN '  HR' ELSE '  HRS' END AS tz_diff
  FROM early_to_late_games g
  CROSS JOIN client c
  ORDER BY early_to_late;
  """)
  st.dataframe(df)

game_clock()