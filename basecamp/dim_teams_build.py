import os, sys
import json
from pathlib import Path
import paths

from api_teams.teams_api import get_teams_info
#from db_teams.teams_db import upsert_teams_data

def main():
  
    teams_info=get_teams_info()
        
    if len(teams_info) > 0:
        print(f"Processing {len(teams_info)} teams")
        
        #upsert_team_data(teams_info)
        
    else:
        print("\n *** No new teams to add from the Teams API *** \n")

if __name__ == '__main__':
    main()
