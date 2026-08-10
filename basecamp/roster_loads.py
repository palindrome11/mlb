import json
import os,sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(BASE_DIR)
RAW_DATA = os.path.join(PROJECT_DIR, "raw_data", "daily_rosters")
ARCHIVE_PATH = os.path.join(RAW_DATA, "archive")
ACTIVE_ROSTER_SIZE = 26  # Expected number of players in the active roster
DH_ACTIVE_ROSTER_SIZE = 27  # Expected number of players in the active roster with DH
sys.path.insert(0, PROJECT_DIR)

from bus_rosters.roster_u import deduplicate_files
#from bus_rosters.roster_u import check_roster_size
from bus_rosters.roster_u import archive_files
from bus_rosters.rosters_db import upsert_roster_snapshot_data

file_glob='roster_snapshot_*.json'

proc_files = deduplicate_files(RAW_DATA,file_glob)
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
    loaded.append(f)
    print(loaded)   
    
    # roster_size = check_roster_size(roster,ACTIVE_ROSTER_SIZE)
    # if roster_size == ACTIVE_ROSTER_SIZE:
    #     upsert_data(roster)
    #     loaded.append(f)
    #     archive_files(loaded)
    # if roster_size == DH_ACTIVE_ROSTER_SIZE:    
    #     upsert_data(roster)
    #     loaded.append(f)
    #     archive_files(loaded)
    
    
    upsert_roster_snapshot_data(roster)
    archive_files(loaded,ARCHIVE_PATH)
    
