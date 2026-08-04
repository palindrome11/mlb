import json
import statsapi
from datetime import datetime, date
import pandas as pd
import os


def current_roster_text(team_id):
        roster=statsapi.roster(team_id)
        return(roster)

def current_roster_json(team_id):
    roster = statsapi.get('team_roster', {'teamId': team_id})
    return(roster)

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

##Pretty Print the Roster List
#current_roster_data = current_roster_text(111)
#print(current_roster_data)

##Get the Roster as JSON
current_roster_data = current_roster_json(111)
print(json.dumps(current_roster_data, indent=2))

#print(type(current_roster_data))       # <class 'dict'> → keys, not positions
#print(current_roster_data.keys())      # dict_keys(['copyright', 'roster', 'link', 'teamId', 'rosterType'])

"""
print(current_roster_data['copyright'])  # first key in the dict
print(current_roster_data['roster'])
print(current_roster_data['link'])       # last key in the dict
print(current_roster_data['teamId'])    
print(current_roster_data['rosterType'])

print(json.dumps(current_roster_data['roster'][0], indent=2))  # first player in the roster list
"""

"""
THIS CODE MoVED TO the api_get_roster.py file
    
#print(json.dumps(current_roster_data['roster'][0], indent=2))  # first player in the roster list
roster = capture_roster(team_id=111)
#print(json.dumps(roster, indent=2))
raw_data = "/Users/cwconlon/@dev/mlb/raw_data/daily_rosters"
os.makedirs(raw_data, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
fname = f"roster_snapshot_{timestamp}.json"
with open(os.path.join(raw_data, fname), 'w') as f:    
    json.dump(roster, f, indent=2)
    print(f"Roster snapshot saved to {os.path.join(raw_data, fname)}")

"""
    
    
   


