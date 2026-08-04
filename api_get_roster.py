import json
import statsapi
from datetime import datetime, date
import os

def capture_roster(team_id):
    snapshot_date = date.today().isoformat()   #
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

teams = [111,121,131,141,151,161,171,181,191,201,211,221,231,241,251,261,271,281,291,301,311,321,331,341,351,361,371,381]
selected_teams=[111]  # Example: only capture rosters for these teams
for team_id in selected_teams: 
    roster = capture_roster(team_id)
    raw_data = "/Users/cwconlon/@dev/mlb/raw_data/daily_rosters"
    os.makedirs(raw_data, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"roster_snapshot_{team_id}_{timestamp}.json"
    with open(os.path.join(raw_data, fname), 'w') as f:    
        json.dump(roster, f, indent=2)
        print(f"Roster snapshot saved to {os.path.join(raw_data, fname)}")