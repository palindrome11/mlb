from curses import raw
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json
import os
import sys
import re
from pathlib import Path
from paths import RAW_DATA, ARCHIVE_PATH
from bus_rosters.roster_u import deduplicate_files, archive_files
from db_rosters.rosters_db import insert_roster_capture_data, upsert_roster_snapshot_data

FILE_GLOB = 'roster_snapshot_*.json'
LOCAL_TZ = ZoneInfo("America/New_York")
PATTERN = re.compile(r"roster_snapshot_(\d+)_(\d{14})\.json$")

roster_type = "Active"
captured_at_inferred = False

def parse_filename(path: Path) -> tuple[int, datetime]:
    """-> (team_id, captured_at in UTC). Raises if the name doesn't match."""
    m = PATTERN.search(Path(path).name)
    if not m:
        raise ValueError(f"Unexpected filename: {Path(path).name}")

    team_id, stamp = int(m.group(1)), m.group(2)
    local = datetime.strptime(stamp, "%Y%m%d%H%M%S").replace(tzinfo=LOCAL_TZ)
    return team_id, local.astimezone(timezone.utc)

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    proc_files = deduplicate_files(RAW_DATA, FILE_GLOB)
    #print(proc_files)
    #team_id, captured_at = parse_filename(proc_files[0])
    #print(f"team_id: {team_id}, captured_at: {captured_at.isoformat()}")
    
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


        #upsert_roster_snapshot_data(roster)
        
        team_id, captured_at = parse_filename(f)
        roster_capture_info = {
            "captured_at": captured_at,
            "captured_at_inferred": captured_at_inferred,
            "team_id": team_id,
            "roster_type": roster_type,
            "source_file": f.name,
            "player_count": len(roster)
        }
        roster_players = [
            {
                "player_id": p["player_id"],
                "player_name": p["player_name"],
                "position": p.get("position"),
                "status": p.get("status")
            }
            for p in roster
        ]
        insert_roster_capture_data(roster_capture_info, roster_players)
        upsert_roster_snapshot_data(roster)
        loaded.append(f)

    if loaded:
       archive_files(loaded, ARCHIVE_PATH)
       print(f"Archived {len(loaded)} file(s)")
    else:
       print("No files loaded — nothing archived")


if __name__ == '__main__':
    main()

