
WITH pairs AS (
  SELECT capture_id, team_id, captured_at,
         LAG(capture_id) OVER (PARTITION BY team_id, roster_type ORDER BY captured_at) AS prev_id
  FROM roster_captures
  WHERE roster_type = 'Active'
)
SELECT p.team_id, p.captured_at, x.player_id, x.player_name, x.change
FROM pairs p
CROSS JOIN LATERAL (
    (
      SELECT player_id, player_name, 'added' AS change
      FROM roster_capture_members WHERE capture_id = p.capture_id
      EXCEPT ALL
      SELECT player_id, player_name, 'added'
      FROM roster_capture_members WHERE capture_id = p.prev_id
    )
    UNION ALL
    (
      SELECT player_id, player_name, 'removed'
      FROM roster_capture_members WHERE capture_id = p.prev_id
      EXCEPT ALL
      SELECT player_id, player_name, 'removed'
      FROM roster_capture_members WHERE capture_id = p.capture_id
    )
) x
WHERE p.prev_id IS NOT NULL
ORDER BY p.captured_at, x.change;