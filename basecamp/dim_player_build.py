import os, sys
import json
from pathlib import Path
import paths

from bus_rosters.roster_u import get_roster_player_ids
from api_people.people_api import get_player_info
from db_people.people_db import upsert_player_data

def main():
    #Get the new players from the last roster database load
    player_ids=get_roster_player_ids()
    ## player_ids=[592450, 592451, 592452, 592453]

    ##Test Data
    ##player_ids=[592450, 592451, 592452, 592453]
    ##ids = ','.join(map(str, player_ids))

    #Test player_ids
    #player_ids=[592450, 592451]

    if len(player_ids) > 0:
        print(f"\nProcessing {len(player_ids)} Players")
        ids = ','.join(map(str, player_ids))
        players_data=get_player_info(ids)
        
        #Test Output Code
        # for player in players_data:
        #     print('***********')
        #     for f , v in player.items():
        #        print(f"{f}: ,{v}")
        
        upsert_player_data(players_data)
        
    else:
        print("\n *** No new players to add from the Rosters *** \n")

if __name__ == '__main__':
    main()
