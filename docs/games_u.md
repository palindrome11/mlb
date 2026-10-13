# GAMES

## Utility Functions For Games

### games_u.py - Utility Functions for Games - in bus_games.

**get_game_team_ids()**

This one returns tuples of the team ids for a game or games that are being played on a certain date. The tuples will be returned in a list for the away and home teams for the day specified. 

Specify with the --date argument in 'YYY-MM-DD' format as an argument to the program.

Use this function to retrieve the team_ids in tuples of the teams playing each other on a given day.

Most often this function will be used in conjunction with a driver program to provide the teams playing games on a certain day. 


## Streamlit web app to populate a suite of games 

The most common suite of games would be to populate the games for am individual season either historically or contemporaneously. The application allows for selection based on dates, date ranges, season (Spring Training, Regular Season, Post Season) and individual or groups of teams or all teams can be selected. 

The app will populate either a development database or a production database based on GUI selection.

It populates the dim_games database table using the game_pk (primary key) 
and the following selected attributes for each game:

- game_pk
- season 
- game_type 
- official_date
- game_datetime 
- home_team_id
- away_team_id 
- venue_id 
- coded_game_state 
- day_night 
- doubleheader 
- game_number
- resumed_from
- rescheduled_from

The web app is invoked from the project directory (mlb) into a web browser using Streamlit in the python environment. The Streamlit apps are always prefixed with an 'sl' and most often are located in the basecamp subdirectory that is one below the project root. In this case, the program is named, sl_games_build.py and is invoked via the local python venv as **`streamlit run basecamp/sl_games_build.py`**

## Streamlit app to display today's games with venue and local times

On invocation, a list of all games to be played or played on a given day are shown on the web page with both the venue time and the local time of the user with a countdown clock until the start of each game. 

The web app is invoked from the project directory (mlb) into a web browser using Streamlit in the python environment. The Streamlit apps are always prefixed with an 'sl' and most often are located in the basecamp subdirectory that is one below the project root. In this case, the program is named, sl_gameclock.py and is invoked via the local python venv as **`streamlit run basecamp/sl_gameclock_.py`**
