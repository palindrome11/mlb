The daily games are loaded into dim_games via a cron job that is programmed to execute every day at every hour from hour 8 to Hour 23 that will execute according to the host machine clock. These times are set to be congruent with Eastern time zone of the United States as outside of the rare game that is played in Europe, most all games can be captured by using the United States Eastern Time Zone as the starting point for the API retrieval. 

Game times can change right up until the game is set to be played, so it is capturing from 8 AM in the morning to 11 PM at night Eastern and is going to get all the games.

crontab entry:
01 8-23 * * * /Users/cwconlon/@dev/mlb/bin/todays_games_load.sh >> /Users/cwconlon/@dev/mlb/logs/daily.log 2>&1

In order to see the games in chronological order of play, there is an SQL query included called 'TodaysGamesChronologialStart.sql' which will list them in order of their play and with the local time of the venue for the Home team displayed.

--- Query:

WITH early_to_late_games AS 
  (
  SELECT
   g.game_pk AS game_pk
  ,ht.name AS home_team 
  ,wt.name AS away_team 
  ,g.official_date AS official_date
  ,to_char(g.game_datetime AT TIME ZONE v.time_zone_id, 'FMHH12:MI AM') AS local_start
  ,v.time_zone_id AS timezone
  ,v.name AS venue
  ,CONCAT(v.city, ' , ', v.state, NULL) AS locale
  ,row_number() OVER (ORDER BY g.game_datetime) AS early_to_late
FROM dim_games g
JOIN dim_teams ht ON ht.team_id = g.home_team_id
JOIN dim_teams wt ON wt.team_id = g.away_team_id
JOIN dim_venues v ON v.venue_id = g.venue_id
WHERE official_date = current_date
)
SELECT 
game_pk
,official_date
,away_team
,home_team
,local_start
,timezone
,venue
,locale
FROM early_to_late_games
ORDER BY early_to_late

--- End of query

`dim_games_build.py`
The Driver program called by cron or independently:
basecamp. -- This program can be found in the basecamp directory
  
Although called by cron each day, this program can be run independently with command line arguments. The command line arguments are:

"--date", nargs="+", type=date.fromisoformat, metavar="YYYY-MM-DD",
         help="One or more individual dates",

"--date_range", nargs=2, type=date.fromisoformat, metavar=("START", "END"),
        help="Inclusive start and end date",
        
"--phase",
        nargs="+",
        choices=sorted(PHASE_TO_TYPES),
        default=["regular"],
        help="Game types to load (default: regular)",
     
"--dry_run",
    action="store_true",
    help="Print the windows that would be fetched, then exit without calling the 
    API"


Similar to Roster construction, their are two phases to processing the games:

`games_stage.py` execs the API call and retrieves the games in json formatted files which are placed in the `raw_data/games` directory as staged files. Then a second program is calle `game_loads.py` for upsert to the Postgres database and that being specifically the dim_games table. The infrastrure is there to archive these filesbut it is not enabled by default. SO, once the games data has been inserted to the database, the original json files are deleted. This is the same as Roster processing except the rosters json files are being archived since they are volatile on a day by day basis during the season and we are capturing that activity dor analysis which otherwise would be gone.














































































































































































































































































































































































































































































