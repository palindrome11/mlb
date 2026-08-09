import json
import statsapi


def full_year_game_summaries(team_id):
    games = statsapi.schedule(team_id, start_date='01/01/2026', end_date='07/28/2026')
    for g in games:
        print(g['summary'])

def reg_season_game_summaries(team_id):
    games = statsapi.schedule(team=team_id, start_date='03/26/2026', end_date='07/28/2026')
    for g in games:
        print(g['summary'])

def red_sox_games():
    team_info = statsapi.lookup_team('red sox')
    print(team_info)
    team_id = statsapi.lookup_team('red sox')[0]['id']
    reg_season_game_summaries(team_id)

def full_team_meta():
    data = statsapi.get('teams', {'sportId': 1})   # sportId 1 = MLB
    return(data)

def team_ids(data):
    teams = [(t['id'], t['name']) for t in data['teams']]
    return(teams)

data=full_team_meta()
#print(json.dumps(data, indent=2))
team_ids=team_ids(data)
for t in team_ids:
    print(json.dumps(t))