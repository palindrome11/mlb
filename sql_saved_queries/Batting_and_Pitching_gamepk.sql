SELECT
official_date
,p.full_name
,pitch.*
FROM fact_pitching pitch
JOIN dim_players p
 ON p.player_id = pitch.player_id
JOIN dim_games g
 ON g.game_pk = pitch.game_pk
WHERE g.game_pk = 822845
-- WHERE official_date = '2026-09-17'

SELECT 
official_date
,p.full_name
,bat.*
FROM fact_batting bat
JOIN dim_players p
 ON p.player_id = bat.player_id
JOIN dim_games g
 ON g.game_pk = bat.game_pk
WHERE g.game_pk = 822845
-- WHERE official_date = '2026-09-17'

