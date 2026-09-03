
# Filename: -> roster_u.py
## Functions
- **get_roster_player_ids():**
  
    This function will return the player_id(s) from the roster_snapshots Posrgres table It returns the records that have been added to the roster(s) but not added to the dim_players yet. It left joins the current roster_snapshot with the current dim_players and returns those player_id(s) that are added to the roster but not yet accounted for in the players_dim.

    ```sql
    SELECT DISTINCT r.player_id
    FROM roster_snapshots r
    LEFT JOIN dim_players d ON d.player_id = r.player_id
    WHERE d.player_id IS NULL;
    ```

    Either the operating system environment vairiables or the .env file with Postgres access details needs to be in place in the project directory (one level above) for seemless access out of the box. Otherwise just update the code in the function to reflect where your project directory and .env are located.



