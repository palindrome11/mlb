# Daily MLB Roster and Box Score Data

## Overview

This project is designed to expose player, game, and team data available from multiple sources with the core reference being the publicly available MLB-StatsAPI (https://github.com/toddrob99/MLB-StatsAPI/wiki) maintained by Major League Baseball (MLB).

The programming is designed with the goal of organizing and exposing the data from roster updates and game by game Box Score statistics for ad-hoc analysis via SQL queries. Using a Postgres database, a star table design uses fact tables of game by game player performance statistics with dimension tables for players, teams, venues, games and Dates. It is designed to track the 30 MLB teams and players through Spring Training, the Regular Season and the Playoffs whether it be for historical or near real time purposes.

Each of the Python programs that work with the MLB Stats API or the Postgres database are designed to operate in a standalone mode or as imports. 

## Project Directory Layout

The project directory is the choice of the installer. In the default installation it is called ```mlb``` as it is depicted below. Wherever in the file system that the project directory is placed and whatever it is called, it becomes the anchor for the subdirectory structure that is required below it.

### Project Root
``` mlb/ ```
#### API Endpoint Retrieval and Processing 
```
├── api_boxscore
├── api_games
├── api_people
├── api_rosters
├── api_seasons
├── api_teams
├── api_venues
```

#### Driver programs that build and execute the ETL pipelines 
```── basecamp```
#### Shell Scripts that build and execute the ETL pipelines  
```── bin```
#### Utilities and Extras For ETL Endpoint data 
```
├── bus_game
├── bus_games
├── bus_people
├── bus_rosters
├── bus_teams
├── bus_venues
```
#### Postgres Database CRUD Processing
```
├── db_batting
│   └── db_utils
├── db_boxscore
│   └── db_utils
├── db_dates
│   └── db_utils
├── db_games
│   └── db_utils
├── db_people
│   └── db_utils
├── db_pitching
│   └── db_utils
├── db_rosters
│   └── db_utils
├── db_seasons
│   └── db_utils
├── db_teams
│   └── db_utils
├── db_venues
│   └── db_utils
```
#### Documentation
```
├── docs
│   
```
#### logs
```
├── logs
```
#### Raw Data 
```
├── raw_data
│   ├── daily_rosters
│   │   └── archive
│   └── games
│       └── archive
```
#### SQL Queries and General Processing Routines 
```
├── sql
```
#### General Utility programs 
```
└── utils 
```

## API Retrieval

A Python program retrieves JSON directly from the endpoint usually using one of the .get methods available. From an organizational perspective, the established convention is to **create a directory** one level below the project root and name it with the general name of the endpoint. Thus the games endpoint subdirectory would be `api_games` following the pattern of `api_<name of the endpoint>`. 

The following are the MLB Stats endpoints with their api interface programs listed within the module subdirectories.

```
api_rosters:
total 8
-rw-r--r--@  1 cwconlon  staff     0 Sep  3 13:35 __pycache__
drwxr-xr-x@  4 cwconlon  staff   128 Sep  3 13:35 .
drwxr-xr-x@ 57 cwconlon  staff  1824 Sep 18 17:53 ..
-rw-r--r--@  1 cwconlon  staff  1985 Sep 16 15:50 rosters_api.py

api_seasons:
total 8
drwxr-xr-x@  3 cwconlon  staff    96 Sep  4 11:15 __pycache__
drwxr-xr-x@  4 cwconlon  staff   128 Sep  4 11:15 .
drwxr-xr-x@ 57 cwconlon  staff  1824 Sep 18 17:53 ..
-rw-r--r--@  1 cwconlon  staff   759 Sep  3 13:35 season_api.py

api_teams:
total 8
-rw-r--r--@  1 cwconlon  staff     0 Sep  3 13:35 __pycache__
drwxr-xr-x@  4 cwconlon  staff   128 Sep  3 13:35 .
drwxr-xr-x@ 57 cwconlon  staff  1824 Sep 18 17:53 ..
-rw-r--r--@  1 cwconlon  staff  1267 Sep  3 13:35 teams_api.py

api_venues:
total 8
drwxr-xr-x@  3 cwconlon  staff    96 Sep  3 14:21 __pycache__
drwxr-xr-x@  4 cwconlon  staff   128 Sep  3 14:21 .
drwxr-xr-x@ 57 cwconlon  staff  1824 Sep 18 17:53 ..
-rw-r--r--@  1 cwconlon  staff  3530 Sep  3 13:35 venues_api.py
```

## Database Structure and Processing

The main database is called `mlb` in this project, but it could be anything the installer chooses. A .env file in the project root directory specfies the credentials and database name for any implementation specific environment. Each site will, of course, have it's own specific credentials and will need to populate it's own .env file in the project root. An example .env file is included to illustrate the most common parameters required for a Postgres implementation:

		# .env.example — copy to .env and fill in
		DB_HOST=<site specific address or name>
		DB_NAME=<site specific database name>
		DB_USER=<site specific DB administrative user name>
		DB_PASSWORD=<site specific DB password>

The subdirectory structure for the database programming is divided into functional areas that roughly correspond to the database tables created to effect the star design for statistical analysis as depicted below:

```
| table_schema | table_name             |  Subdirectory Processing
| ------------ | ---------------------- |
| public       | boxscore_raw           |   --> db_boxscore
| public       | dim_date               |   --> db_dates
| public       | dim_games              |   --> db_games
| public       | dim_players            |   --> db_people
| public       | dim_seasons            |   --> db_seasons
| public       | dim_teams              |   --> db_teams
| public       | dim_venues             |   --> db_venues
| public       | fact_batting           |   --> db_batting
| public       | fact_pitching          |   --> db_pitching
| public       | roster_capture_members |   --> db_rosters
| public       | roster_captures        |   --> db_rosters
| public       | roster_snapshots       |   --> db_rosters
```

The delivery and maintenance of data to the database tables is accomplished by the Python programs in these subdirectories. For the most part, these programs are designed to take a Dictionary, CSV or JSON file and create, replace, update or delete the tables and table entries.

One subdirectory below the DB processing directories there is also `db_utils` subdirectory that contains the original table creation code via SQL CREATE statements and/or sql dump files. 


## Drivers
This code lives in the subdirectory `basecamp`. These programs accomplish specific ETL processing for raw data ingested and format it to handoff to the database processing programs. 



