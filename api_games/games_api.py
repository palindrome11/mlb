import statsapi
import argparse
from datetime import datetime
import json
import os,sys
import paths

def capture_schedule(start_date, end_date, sport_id=1):
    """Return the raw schedule payload for a date range (YYYY-MM-DD strings)."""
    return statsapi.get('schedule', {
        'sportId': sport_id,
        'startDate': start_date,
        'endDate': end_date,
    })



# SEARCH GOOGLE:  mlb sats api document api/v1/schedule%253FsportId=1&startDate=&endDat

# Endpoint OverviewBase 
# URL: https://statsapi.mlb.com/api/v1/schedule
# 
# Authentication: None required (publicly accessible)
# 
# Method: GET

#ParameterssportId: 1 represents Major League Baseball (MLB)
# .startDate: Format as YYYY-MM-DD (e.g., 2026-08-22)
# .endDate: Format as YYYY-MM-DD (can match startDate for a single day)
# .hydrate (optional): Pass additional data strings like team, lineups, or venue (e.g., &hydrate=team).

# json{
#   "copyright": "Copyright 2026 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms of use.",
#   "totalItems": 1,
#   "totalEvents": 0,
#   "totalGames": 1,
#   "totalGamesInProgress": 0,
#   "dates": [
    # {
    #   "date": "2026-08-22",
    #   "totalItems": 1,
    #   "totalEvents": 0,
    #   "totalGames": 1,
    #   "totalGamesInProgress": 0,
    #   "games": [
    #     {
    #       "gamePk": 745712,
    #       "gameGuid": "6f2d9c12-3a4b-5c6d-7e8f-9a0b1c2d3e4f",
    #       "link": "/api/v1/game/745712/feed/live",
    #       "gameType": "R",
    #       "season": "2026",
    #       "gameDate": "2026-08-22T23:05:00Z",
    #       "officialDate": "2026-08-22",
    #       "status": {
    #         "abstractGameState": "Preview",
    #         "codedGameState": "S",
    #         "detailedState": "Scheduled",
    #         "statusCode": "S",
    #         "startTimeTBD": false,
    #         "abstractGameCode": "P"
    #       },
    #       "teams": {
    #         "away": {
    #           "leagueRecord": {
    #             "wins": 65,
    #             "losses": 60,
    #             "pct": ".520"
    #           },
    #           "team": {
    #             "id": 147,
    #             "name": "New York Yankees",
    #             "link": "/api/v1/teams/147"
    #           },
    #           "splitSquad": false,
    #           "seriesNumber": 40
    #         },
    #         "home": {
    #           "leagueRecord": {
    #             "wins": 70,
    #             "losses": 55,
    #             "pct": ".560"
    #           },
    #           "team": {
    #             "id": 111,
    #             "name": "Boston Red Sox",
    #             "link": "/api/v1/teams/111"
    #           },
    #           "splitSquad": false,
    #           "seriesNumber": 40
    #         }
    #       },
    #       "venue": {
    #         "id": 3,
    #         "name": "Fenway Park",
    #         "link": "/api/v1/venues/3"
    #       },
    #       "content": {
    #         "link": "/api/v1/game/745712/content"
    #       },
    #       "gameNumber": 1,
    #       "publicFacing": true,
    #       "doubleHeader": "N",
    #       "gamedayType": "P",
    #       "tiebreaker": "N",
    #       "calendarEventID": "14-745712-2026-08-22",
    #       "seasonDisplay": "2026",
    #       "dayNight": "N",
    #       "scheduledInnings": 9,
    #       "reverseHomeAwayStatus": false,
    #       "inningBreakLength": 120,
    #       "gamesInSeries": 3,
    #       "seriesGameNumber": 2,
    #       "seriesDescription": "Regular Season",
    #       "recordSource": "MLB",
    #       "ifNecessary": "N",
    #       "ifNecessaryDescription": "Normal Game"
#     #     }
#       ]
#     }
#   ]
# }

def valid_date(date_string):
    try:
        # Enforces the YYYY-MM-DD format strictly
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        # Raises a clean error message back to the CLI user
        raise argparse.ArgumentTypeError(f"Not a valid date: '{date_string}'. Expected format: YYYY-MM-DD.")

def main():
    parser = argparse.ArgumentParser(description="Please input start date and end date for range of game data to retrieve")
    parser.add_argument("start_date", type=valid_date, help="Game Start Date in the format YYYY-MM-DD")
    parser.add_argument("end_date", type=valid_date, help="Game End Date in the format YYYY-MM-DD")
    args = parser.parse_args()
    
    print(f"Start Date: {args.start_date} End Date: {args.end_date}")
    game_schedule_data = capture_schedule(args.start_date, args.end_date)
    print(game_schedule_data)


if __name__ == "__main__":
  main()