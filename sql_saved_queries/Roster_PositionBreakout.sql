SELECT
    snapshot_date,
    COUNT(*) AS roster_size,
    SUM(CASE WHEN position = 'P' THEN 1 ELSE 0 END) AS pitchers,
    SUM(CASE WHEN position <> 'P' THEN 1 ELSE 0 END) AS position_players
FROM roster_snapshots
GROUP BY snapshot_date
ORDER BY snapshot_date;









