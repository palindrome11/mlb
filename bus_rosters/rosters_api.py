import statsapi
from datetime import datetime, date

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