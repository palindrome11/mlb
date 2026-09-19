WITH early_to_late_games AS 
  (
  SELECT
   g.game_pk AS game_pk
  ,ht.name AS home_team 
  ,wt.name AS away_team 
  ,g.official_date AS official_date
  ,to_char(g.game_datetime AT TIME ZONE v.time_zone_id, 'FMHH12:MI AM') AS local_start
  ,v.time_zone_id AS timezone
  ,v.name AS venue
  ,CONCAT(v.city, ' , ', v.state, NULL) AS locale
  ,row_number() OVER (ORDER BY g.game_datetime) AS early_to_late
FROM dim_games g
JOIN dim_teams ht ON ht.team_id = g.home_team_id
JOIN dim_teams wt ON wt.team_id = g.away_team_id
JOIN dim_venues v ON v.venue_id = g.venue_id
WHERE official_date = current_date
)
SELECT 
game_pk
,official_date
,away_team
,home_team
,local_start
,timezone
,venue
,locale
FROM early_to_late_games
ORDER BY early_to_late