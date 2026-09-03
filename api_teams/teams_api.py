import json
import statsapi
from datetime import datetime, date
import os
import paths


# Endpoint: teams
# URL: https://statsapi.mlb.com/api/{ver}/teams
# Required Parameters
# None
# All Parameters
# ver
# season
# activeStatus
# leagueIds
# sportId
# sportIds
# gameType
# hydrate
# fields

def get_teams_info():
    #API CALL
    #This gets all the teams
    data = statsapi.get('teams', {'sportId': 1})
    #print(f"{len(data['teams'])} teams")
    #print(json.dumps(data['teams'][1], indent=2))   
    #print(data)
    teams_data=[]
    for p in data['teams']:
        teams_data.append({
        'team_id': p['id'],
        'name': p['name'],
        'team_code': p['teamCode'],
        'abbreviation': p['abbreviation'],
        'club_name': p['teamName'],
        'location_name': p['locationName'],
        'league_id': p['league']['id'],
        'league_name': p['league']['name'],
        'division_id': p['division']['id'],
        'division_name': p['division']['name'],
        'venue_id': p['venue']['id'],
        'venue_name': p['venue']['name'],
        'first_year': p['firstYearOfPlay'],
        'active': p['active']})
    return(teams_data)
    

if __name__ == '__main__':        
    team_db_data = get_teams_info()
    print(team_db_data)

