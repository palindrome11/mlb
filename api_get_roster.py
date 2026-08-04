import json
import statsapi
from datetime import datetime, date
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA = os.path.join(BASE_DIR, "raw_data", "daily_rosters")

def capture_roster(team_id):
    snapshot_date = date.today().isoformat()
    data = statsapi.get('team_roster', {'teamId': team_id, 'rosterType': 'active'})
    rows = []
    for p in data['roster']:
        rows.append({
            'snapshot_date': snapshot_date,
            'team_id': team_id,
            'player_id': p['person']['id'],
            'player_name': p['person']['fullName'],
            'position': p['position']['abbreviation'],
            'status': p.get('status', {}).get('description'),
        })
    return rows

if __name__ == '__main__':                      # ← the guard
    os.makedirs(RAW_DATA, exist_ok=True)
    selected_teams = [111]
    for team_id in selected_teams:
        roster = capture_roster(team_id)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        fname = f"roster_snapshot_{team_id}_{timestamp}.json"
        fpath = os.path.join(RAW_DATA, fname)
        with open(fpath, 'w') as f:
            json.dump(roster, f, indent=2)
        print(f"Roster snapshot saved to {fpath}")