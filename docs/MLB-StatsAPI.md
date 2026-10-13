# MLB-StatsAPI 

MLB-StatsAPI is a Python wrapper around Major League Baseball's 
official Stats API  <http://statsapi.mlb.com>. 

It provides free, keyless access to MLB data as delineated in the below list.

- schedules
- live and historical scores
- box scores
- player and team stats
- standings
- rosters
- transactions — going back decades.


The library exposes two levels of access:

1. Convenience functions (schedule(), roster(), standings(), boxscore_data(), lookup_team(), lookup_player()) that return formatted text or simplified Python structures for common queries.
2. A low-level get() function that hits any raw API endpoint and returns full nested JSON, suitable for programmatic use and data pipelines.


Key characteristics:
- No authentication or API key required — public endpoints
- Historical depth — supports date-based queries, including point-in-time roster snapshots
- Returns nested JSON (lists of dicts) mirroring MLB's data model: teams, venues, games, players as related entities with stable numeric IDs (e.g., Red Sox = 111)

## The MLB-StatsAPI Wiki: 
<https://github.com/toddrob99/MLB-StatsAPI/wiki>

This documents every wrapper function with parameters, defaults and example calls. 

The "Endpoints" page lists all the raw API endpoints accessible via statsapi.get() with required and optional parameters, and hydrations.

JSON payloads are returned via the API endpoints but are not documented in the WIKI. As desribed in the README.md file for this project, shedding light on the returned data and placing it in an accessible, useful group of frameworks for Data Analysis is a large part of the reason for this project.

For a further understanding of some of the techniques used by us to interpret the JSON returned data payloads please refer to the document - ParsingJSON.md.
 


