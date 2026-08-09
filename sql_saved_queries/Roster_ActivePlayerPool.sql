WITH active_player_pool as
  (
  SELECT 
  DISTINCT r1.player_name
  FROM roster_snapshots r1
  LEFT JOIN roster_snapshots r2
   ON r1.player_id = r2.player_id
  )
SELECT 
* 
FROM active_player_pool app








