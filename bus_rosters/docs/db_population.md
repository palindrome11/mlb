## Populating the MLB database: ##

1. Populate dim_teams with data

This is done by running `dim_teams_build.py` in the basecamp directory.This will populate the teams database with basic information about each of the MLB teams for a season by asking for the season to populate from the command line. So, run the program, input the season year, and voi;a all the teams relevant to that regular season in the mlb are populated in the table.

2. Populate dim_venues with data

This is done by running `dim_venues_build.py` in the basecamp directory. It accepts two command line arguments:
`--venue-ids`
Populates the dim_venues table individually if the venue primary key(PK) is known.  
`--active-venue_ids`
This will populate the venues database with the active teams for the given season. Active teams are determined via the program `venue_id_search` in the utilities subdirectory `bus_venues`. The routine takes the UNION of the venue_id fields in the dim_games and dim_teams. So, in other words, this gets the home ballparks for all 30 teams amd any ballparks/places that were played outside of those main parks such as "The Field Of Dreams".

3. Populate dim_seasons with data

This is done by running `dim_seasons_build.py` in the basecamp directory. THis populates a single record with all of the dates relevant to the start and end of the various seasons (pre-season, regular_season, post_season, off_season. 

4. Populate dim_games with data

There are many choices here regarding what level of granularity in time (today,yesterday) or a date range or a full season. Also, choices can be made on the basis of pre-season, post-season, regular-season bringing in the dim_seasons table to demarcate the boundaries of each recognized date grouping. 

As a means of allowing the user to select criteria relevant to their needs, there is a streamlit app that allows selection from among these choices to create a customized data grouping. Although the common case is likely regular season for a given year, there are many permutations of multiple seasons games, subsets of a certain season's games or just games that are belong to pre-season or post-season. The web interface (streamlit app) is designed to allow for these customizations to be communicated tot he driver programs so that database tables can be updated to reflect the customizations. On the other hand there are common scenarios that can be built with just running a single python program from the command like a full 'regular season' set of games for a given year.

5. Populate dim_date with data

The dim_date table is pretty much a static dimension table designed ot provide an easy way to get the attributes of a day without having to go through hoops of extraction and formatting. Populate this table via the driver program in the basecamp subdirectory and it will fill in the data for every daya from 01/01/2020 to 12/31/2035. It will alos do the season overlays on the dates marking the starting and ending dates of the pre-season, regular_season, and post_season. 


Brady 








	