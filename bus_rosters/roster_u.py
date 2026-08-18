import os
from pathlib import Path

import psycopg2

from paths import PROJECT_DIR          # importing paths also loads .env
import utils.test_files_match as test_files


def get_roster_player_ids():
    """Player IDs present in roster_snapshots but missing from dim_players."""
    RETRIEVE_SQL = """
        SELECT DISTINCT r.player_id
        FROM roster_snapshots r
        LEFT JOIN dim_players d ON d.player_id = r.player_id
        WHERE d.player_id IS NULL;
    """

    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
    )
    try:
        with conn, conn.cursor() as cur:
            cur.execute(RETRIEVE_SQL)
            rows = cur.fetchall()
    finally:
        conn.close()

    return [row[0] for row in rows]


def deduplicate_files(raw_data, file_glob):
    seen = {}
    for f in sorted(Path(raw_data).glob(file_glob)):
        digest = test_files.file_checksum(f)
        if digest in seen:
            print(f"Duplicate of {seen[digest].name}: {f.name}")
            f.unlink()
        else:
            seen[digest] = f

    upload_files = list(seen.values())
    print(f"Unique files to upload: {[f.name for f in upload_files]}")
    return upload_files


def archive_files(proc_files, archive_path):
    archive_path.mkdir(parents=True, exist_ok=True)
    for f in proc_files:
        target = archive_path / f.name
        f.rename(target)
        print(f"Archived {f.name} to {target}")


if __name__ == '__main__':        
    pass

