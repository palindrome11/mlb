import psycopg2
import json
import os
from pathlib import Path
import test_files   
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA = os.path.join(BASE_DIR, "raw_data", "daily_rosters")
ARCHIVE_PATH = os.path.join(RAW_DATA, "archive")

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
    
    load_dotenv(os.path.join(BASE_DIR, '.env'))
    
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST','localhost'),
        dbname=os.environ.get('DB_NAME','mlb'),
        user=os.environ.get('DB_USER','postgres'),
        password=os.environ.get('DB_PASSWORD') 
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany(UPSERT_SQL, roster)
                cur.execute("SELECT COUNT(*) FROM roster_snapshots WHERE snapshot_date = %s",
                            (roster[0]['snapshot_date'],))
                print(f"Rows now in DB for that date: {cur.fetchone()[0]}")
        print("roster_snapshot uploaded to database.")
    finally:
        conn.close()


def archive_files(proc_files):
    os.makedirs(ARCHIVE_PATH, exist_ok=True)
    for f in proc_files:
        archive_file = os.path.join(ARCHIVE_PATH, f.name)
        os.rename(f, archive_file)
        print(f"Archived {f.name} to {archive_file}")


if __name__ == '__main__':          
    #files = list(Path(RAW_DATA).glob('roster_snapshot_*.json'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    proc_files = deduplicate_files(RAW_DATA)
    loaded = []
    for f in proc_files:
        if f.stat().st_size == 0:
            print(f"SKIPPING empty file: {f.name}")
            continue
        try:
            with open(f, 'r') as file:
                roster = json.load(file)
        except json.JSONDecodeError as e:
            print(f"SKIPPING malformed file {f.name}: {e}")
            continue
        if not roster:
            print(f"SKIPPING file with no records: {f.name}")
            continue
        check_roster(roster)
        upsert_data(roster)
        loaded.append(f)
    archive_files(loaded)





