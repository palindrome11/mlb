import json
import os
import sys

from paths import RAW_DATA, ARCHIVE_PATH
from bus_rosters.roster_u import deduplicate_files, archive_files
from db_rosters.rosters_db import upsert_roster_snapshot_data

FILE_GLOB = 'roster_snapshot_*.json'

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    proc_files = deduplicate_files(RAW_DATA, FILE_GLOB)
    loaded = []

    for f in proc_files:
        if f.stat().st_size == 0:
            print(f"SKIPPING empty file: {f.name}")
            continue
        try:
            roster = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f"SKIPPING malformed file {f.name}: {e}")
            continue
        if not roster:
            print(f"SKIPPING file with no records: {f.name}")
            continue

        upsert_roster_snapshot_data(roster)
        loaded.append(f)

    if loaded:
        archive_files(loaded, ARCHIVE_PATH)
        print(f"Archived {len(loaded)} file(s)")
    else:
        print("No files loaded — nothing archived")


if __name__ == '__main__':
    main()

