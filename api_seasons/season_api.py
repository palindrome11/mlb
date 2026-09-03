import statsapi
import json
import os,sys
import paths

def get_season_info(season_id):
    data = statsapi.get('season', {'seasonId': season_id, 'sportId': 1})
    return data['seasons']

 
# Endpoint 
# URL: https://statsapi.mlb.com/api/v1/season
# 
# Authentication: None required (publicly accessible)
# 
# Method: GET



def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1:
        season_year=int(sys.argv[1])
        season_info=get_season_info(season_year)
        for row in season_info:
            for x,y in row.items():
                print(f"{x}: {y}")
    else:
        print("Need Year of Season as YYYY ")
 

if __name__ == '__main__':      
    main()
    
    


