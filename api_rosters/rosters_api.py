import statsapi
from datetime import datetime, date

def capture_roster(team_id=111,roster_type='active',roster_date=date.today().isoformat()):
    snapshot_date = date.today().isoformat()
    data = statsapi.get('team_roster', {'teamId': team_id, 'rosterType': roster_type, 'date': roster_date})
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

def capture_roster_by_date(team_id,roster_date):
    #parsed_date = datetime.strptime(roster_date, "%m/%d/%Y")
    snapshot_date = roster_date.isoformat()
    data = statsapi.get('team_roster', {'teamId': team_id, 'rosterType': 'active', 'date': roster_date})
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

def capture_roster_by_date_by_type(team_id,roster_date,roster_type):
    #parsed_date = datetime.strptime(roster_date, "%m/%d/%Y")
    snapshot_date = roster_date.isoformat()
    data = statsapi.get('team_roster', {'teamId': team_id, 'rosterType': roster_type, 'date': roster_date})
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
