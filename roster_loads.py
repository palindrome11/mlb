import psycopg2
import json
import os
from pathlib import Path
import test_files   

def deduplicate_files(raw_data):
    seen = {}    # checksum → first file with that content
    for f in sorted(Path(raw_data).glob('roster_snapshot_*.json')):
        digest = test_files.file_checksum(f)
        if digest in seen:
            print(f"Duplicate of {seen[digest].name}: {f.name}")
            os.remove(f)
        else:
            seen[digest] = f

    upload_files = list(seen.values())
    print(f"Unique files to upload: {[f.name for f in upload_files]}")
    return upload_files

def deduplicate_files_2(raw_data):
    ### Algo 2 to find unique files based on content (checksum) and avoid duplicates
    upload_files = []
    files = list(Path(raw_data).glob('roster_snapshot_*.json'))
    for f in files:
        if any(test_files.files_match(kept, f) for kept in upload_files):
            print(f"Duplicate file found: {f}. Skipping.")
            # os.remove(f)
        else:
            print(f"Unique file found: {f}. Adding it.")
            upload_files.append(f)

    for upload_file in upload_files:
        print(upload_file)

def check_roster(roster):
    print(type(roster))       # <class 'list'> → list of dicts
    print(len(roster))        # 26 players in the Red Sox roster
    print(roster[0])          # first player in the roster list

def upsert_data(roster):
    UPSERT_SQL = """
    INSERT INTO roster_snapshots (snapshot_date, team_id, player_id, player_name, position, status) 
    VALUES
        (%(snapshot_date)s, %(team_id)s, %(player_id)s,
        %(player_name)s, %(position)s, %(status)s)
    ON CONFLICT (snapshot_date, team_id, player_id) DO NOTHING;
    """
    
    conn = psycopg2.connect(
        host='localhost',
        dbname='mlb',
        user='postgres',
        password='postgres'
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany(UPSERT_SQL, roster)
                cur.execute("SELECT COUNT(*) FROM roster_snapshots WHERE snapshot_date = %s",
                            (roster[0]['snapshot_date'],))
                print(f"Rows now in DB for that date: {cur.fetchone()[0]}")
    finally:
        conn.close()
        print("roster_snapshot uploaded to database.")


def archive_files(proc_files):
    os.makedirs(archive_path, exist_ok=True)
    for f in proc_files:
        archive_file = os.path.join(archive_path, f.name)
        os.rename(f, archive_file)
        print(f"Archived {f.name} to {archive_file}")


archive_path = "/Users/cwconlon/@dev/mlb/raw_data/daily_rosters/archive"
raw_data = "/Users/cwconlon/@dev/mlb/raw_data/daily_rosters"
files = list(Path(raw_data).glob('roster_snapshot_*.json'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

UPSERT_SQL = """
INSERT INTO roster_snapshots (snapshot_date, team_id, player_id, player_name, position, status) 
VALUES
    (%(snapshot_date)s, %(team_id)s, %(player_id)s,
     %(player_name)s, %(position)s, %(status)s)
ON CONFLICT (snapshot_date, team_id, player_id) DO NOTHING;
"""

proc_files = deduplicate_files(raw_data)
for f in proc_files:
    with open(f, 'r') as file:
        roster = json.load(file)
        check_roster(roster)
        upsert_data(roster)
archive_files(proc_files)





