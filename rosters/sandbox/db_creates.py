import psycopg2

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS roster_snapshots (
    snapshot_date  DATE         NOT NULL,
    team_id        INT          NOT NULL,
    player_id      INT          NOT NULL,
    player_name    VARCHAR(100) NOT NULL,
    position       VARCHAR(10),
    status         VARCHAR(50),
    loaded_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (snapshot_date, team_id, player_id)
);
"""

conn = psycopg2.connect(
    host='localhost',
    dbname='mlb',
    user='postgres',
    password='postgres'
)

with conn:
    with conn.cursor() as cur:
        cur.execute(CREATE_SQL)

conn.close()
print("roster_snapshots Table ready.")