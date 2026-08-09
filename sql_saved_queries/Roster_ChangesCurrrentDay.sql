WITH daily_roster_change AS 
  (
  SELECT
  c.snapshot_date AS current_snapshot_date
  ,p.snapshot_date AS previous_snapshot_date
  ,c.player_id AS player_id
  ,c.player_name AS player_name
  ,c.position AS current_player_position
  ,p.position AS previous_player_position
  ,CASE WHEN p.player_id IS NOT NULL THEN 1 ELSE 0 END AS retained_position
  FROM roster_snapshots c
  LEFT JOIN roster_snapshots p
         ON p.snapshot_date = c.snapshot_date - 1
        AND p.team_id       = c.team_id
        AND p.player_id     = c.player_id
        AND p.position      = c.position
  WHERE c.snapshot_date = current_date 
  )
SELECT 
player_id
,player_name
,current_player_position
,CASE WHEN retained_position = 1 THEN 'No Change' 
  WHEN previous_snapshot_date IS NULL THEN 'New Player'
  WHEN previous_player_position != current_player_position THEN 'Position Change'
  ELSE 'Change'
END AS exception_flag
FROM daily_roster_change
ORDER BY exception_flag


  /*
SELECT *
FROM daily_roster_change
*/









