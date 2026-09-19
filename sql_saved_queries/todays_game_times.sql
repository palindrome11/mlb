SELECT
g.official_date
,g.game_datetime AT TIME ZONE v.time_zone_id AS venue_time
,g.game_datetime AT TIME ZONE 'America/New_York' AS eastern_venue_time
,g.game_datetime AS UTC
,game_pk
,home_team_id
,th.club_name
,away_team_id
,ta.club_name
,g.venue_id
,v.name
,v.time_zone_id
FROM dim_games g
JOIN dim_venues v
 ON g.venue_id = v.venue_id
JOIN dim_teams th
  ON g.home_team_id = th.team_id 
JOIN dim_teams ta 
  ON g.away_team_id = ta.team_id
WHERE g.official_date = current_date
