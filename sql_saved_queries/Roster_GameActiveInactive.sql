WITH active_player_pool as
  (
  SELECT 
  DISTINCT r1.player_name
  FROM roster_snapshots r1
  LEFT JOIN roster_snapshots r2
   ON r1.player_id = r2.player_id
  ),
current_actives as
  (
  SELECT 
  player_name
  ,snapshot_date
  FROM roster_snapshots
   WHERE snapshot_date = current_date
  )
SELECT 
app.player_name
,ca.snapshot_date AS game_date
,CASE 
  WHEN ca.snapshot_date IS Null THEN 'INACTIVE'
  ELSE 'ACTIVE' END AS game_status
FROM active_player_pool app
LEFT JOIN current_actives ca
 ON app.player_name = ca.player_name
ORDER BY game_status DESC 











