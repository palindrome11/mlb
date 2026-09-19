## Processing Boxscores ##

Once the games are played or while the games are being played a boxscore record is available to be retrieved via the API. The game boxscore can be retrieved by specifying the game_pk  (Game Primary Key) which is available from the dim_games table for the date and time of the game. Typically to load a boxscore for a specific game, the game_pk is retrieved from dim_games and is fed to the basecamp/bxload_games.py driver program that populates the raw_boxscore table with the json returned from the API call. 

For example, if I wanted to see the boxscore for the Red Sox versus Rangers game on 9/17/2026 I would lookup the game in dim_games and extract the game_pk identifier (822845). Then it is a matter of plugging the game_pk to the basecamp driver program `basecamp.bxload_games.oy` and it populates the raw_json returned by the API into the raw_boxscore table as a JSON-B field. 

The structure of the raw_boxscore table is very simple, consisting of 3 columns:
	game_pk
	fetched_at
	paylood

Where the payload is the returned JSON for the boxscore.

Then in order to populate the fact_batting database table and fact_pitching database table for a particular game, it is a SELECT as such:

SELECT_PAYLOAD = "SELECT payload FROM boxscore_raw WHERE game_pk = %s"

The program `basecamp.boxscore_loads.py` can be used to populate both fact tables for a given game by enterring the game_pk on the command line. 

FLOW:

1. Last night games are loaded via the cron job that loads the games before they are played:
cron:
01 8-23 * * * /Users/cwconlon/@dev/mlb/bin/todays_games_load.sh >> /Users/cwconlon/@dev/mlb/logs/daily.log 2>&1 

The shell script, `todays_games_load.sh` runs the program 
      `basecamp.dim_games_build.py --date "$RUN_DATE" 

The `basecamp.dim_games_build.py` driver program posts all the games with their venues, the adjusted start times for the local area and with a game_state = 'S'.
T 'S' stands for Scheduled.

After the games are played then the `basecamp.dim_games_build.py` must be run again to get the game_state. All completed games will update the database table with a game_state of 'F' for Final. Only Final games will be processed in the next steps of this process flow.

Now, the raw_boxscore table needs to be populated with a game_pk or game_pks.
THis is as easy as invoking the bxload porgram with one or a comma separated list of game_pks. 
Example:
basecamp/bxload_games.py --game_ids 822923
Parsed list: [822923]
Game Number 822923 processing with 1 remaining to process
boxscore_raw: 1 staged, 0 refreshed, 0 failed
_
Next, populate the fact_batting and fact_pitching tables with the game or games boxscore statistics. 
the driver program `basecamp.boxscore_loads.py`
basecamp/boxscore_loads.py --game_ids 822923
822923: 23 batting, 8 pitching
23 batting rows, 8 pitching rows, 0 game(s) not loaded`
--
And away we go....





