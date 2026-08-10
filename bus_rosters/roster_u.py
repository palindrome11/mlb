from datetime import datetime, date
import os
import psycopg2
from dotenv import load_dotenv
import json
import statsapi
from datetime import datetime, date
import os,sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(BASE_DIR)
ROSTERS_DIR =  os.path.join(PROJECT_DIR,"rosters")
sys.path.insert(0, PROJECT_DIR)

def get_roster_player_ids():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR  = os.path.dirname(BASE_DIR)
    ROSTERS_DIR =  os.path.join(PROJECT_DIR,"rosters")
    sys.path.insert(0, PROJECT_DIR)
    
  
    RETRIEVE_SQL = """
    SELECT DISTINCT r.player_id
    FROM roster_snapshots r
    LEFT JOIN dim_players d ON d.player_id = r.player_id
    WHERE d.player_id IS NULL;
    """
   
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST','localhost'),
        dbname=os.environ.get('DB_NAME','mlb'),
        user=os.environ.get('DB_USER','postgres'),
        password=os.environ.get('DB_PASSWORD') 
    )

    with conn:
        with conn.cursor() as cur:
            cur.execute(RETRIEVE_SQL)
            rows=cur.fetchall()

    conn.close()

    player_ids = [row[0] for row in rows]
    #print(player_ids)
    #print(len(player_ids))

    #print(f"player ids: {ids}")
    return(player_ids)


def deduplicate_files(raw_data,file_glob):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR  = os.path.dirname(BASE_DIR)
    ROSTERS_DIR =  os.path.join(PROJECT_DIR,"rosters")
    sys.path.insert(0, PROJECT_DIR)
        
    import utils.test_files_match  as test_files
    from pathlib import Path
    
    seen = {}    # checksum → first file with that content
    for f in sorted(Path(raw_data).glob(file_glob)):
        digest = test_files.file_checksum(f)
        if digest in seen:
            print(f"Duplicate of {seen[digest].name}: {f.name}")
            os.remove(f)
        else:
            seen[digest] = f

    upload_files = list(seen.values())
    print(f"Unique files to upload: {[f.name for f in upload_files]}")
    return upload_files

# def check_roster_size(roster,p_roster_size):
#     #print(type(roster))       # <class 'list'> → list of dicts
#     #print(len(roster))        # 26 players in the Red Sox roster
#     #print(roster[0])          # first player in the roster list
#     roster_size=len(roster)
#     if roster_size == p_roster_size:
#         #keys = roster[0].keys()
#         #print(f"Keys in roster dict: {keys}")
#         return roster_size
#     else:
#         print(f"Unexpected roster size {roster_size}. Expected {p_roster_size}.")
#         return roster_size

def archive_files(proc_files,archive_path):
    os.makedirs(archive_path, exist_ok=True)
    for f in proc_files:
        archive_file = os.path.join(archive_path, f.name)
        print(archive_file)
        os.rename(f, archive_file)
        print(f"Archived {f.name} to {archive_file}")



if __name__ == '__main__':        
    pass

