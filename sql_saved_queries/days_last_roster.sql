WITH current_day_captures AS 
  (
  SELECT
  *
  FROM roster_captures 
  WHERE captured_at::date = CURRENT_DATE 
  ),
curent_day_last_batch AS
  (
  SELECT 
  MAX(capture_id) AS last_capture_id
  FROM current_day_captures
  )
SELECT
captured_at
,player_name
,position
,team_id
,status
FROM roster_capture_members rcm
JOIN curent_day_last_batch cdlb 
  ON cdlb.last_capture_id = rcm.capture_id 
JOIN roster_captures rc
  ON rc.capture_id = rcm.capture_id