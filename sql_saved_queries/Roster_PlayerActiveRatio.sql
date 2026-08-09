WITH params AS (
    SELECT 26.0 AS active_roster_limit
),
counts AS (
    SELECT COUNT(DISTINCT player_name) AS n FROM roster_snapshots
)
SELECT ROUND(c.n / p.active_roster_limit,2) AS player_active_ratio
FROM counts c
CROSS JOIN params p;










