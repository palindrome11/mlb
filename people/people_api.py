import json
import statsapi
from datetime import datetime, date
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(BASE_DIR)

# Endpoint: people
# URL: https://statsapi.mlb.com/api/{ver}/people
# Required Parameters
# personIds
# All Parameters
# ver
# personIds
# hydrate
# fields
# """
# """
# #Test Code Bloc 
# selected_players  =  [655316,678011]
# data = statsapi.get('people', {'personIds': '655316, 678011'})
# print(json.dumps(data, indent=2))


def get_player_batch(players):
    pass

def get_player_info(ids):
    # """ TESTING SEQUENCES
    # player_ids=[592450, 592450, 592450, 592450, 592]
    # ids = ','.join(map(str, player_ids))
    # print(ids)
    # data = statsapi.get('people', {'personIds': ids})
    # """
    #API CALL
    data = statsapi.get('people', {'personIds': ids})

    players_data=[]
    for p in data['people']:
        players_data.append({
            'player_id': p['id'],
            'full_name': p['fullName'],
            'birth_date': p.get('birthDate'),
            'birth_country': p.get('birthCountry'),
            'birth_city': p.get('birthCity'),
            'height': p.get('height'),
            'bat_side': (p.get('batSide') or {}).get('code'),
            'pitch_hand': (p.get('pitchHand') or {}).get('code'),
            'primary_position': (p.get('primaryPosition') or {}).get('abbreviation'),
            'mlb_debut_date': p.get('mlbDebutDate'),
            'primary_number': p.get('primaryNumber'),
            'current_age': p.get('currentAge')
            })
    #print(players_data)
    #print(json.dumps(data['people'][0], indent=2))
    return(players_data)



if __name__ == '__main__':        
    pass

