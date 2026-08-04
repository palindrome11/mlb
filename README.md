In this project, MLB-StatsAPI serves as the extraction point for various Modules.
To read more on the API:  https://github.com/toddrob99/MLB-StatsAPI/wiki

The first module is called Roster Rooters and is designed to keep track of the current 40 man rosters of all the teams as they change on a daily basis. The data pulled from the API is formatted in JSON files that are updated on a daily basis per team. The json files are pulled daily via a python script that processes an entry per player into a Postgres table called roster_snapshots and is built as such:

CREATE TABLE IF NOT EXISTS roster_snapshots (
    snapshot_date  DATE         NOT NULL,
    team_id        INT          NOT NULL,
    player_id      INT          NOT NULL,
    player_name    VARCHAR(100) NOT NULL,
    position       VARCHAR(10),
    status         VARCHAR(50),
    loaded_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (snapshot_date, team_id, player_id)
);
"""

If you already are running a Postgres server then you will want to create a database in order to house the tables.
For the puposes of this repo, I created a database calling it 'mlb' and used the default username (postgres)
You will need to add your particular database name and user,port,host,password into your .env file or create them 
in your OS Context by whatever means your OS allows environment variables to be instantiated. The python programs
will read the .env file if you do not instantiate the operating system environment and you place it in the 
project root and populate it with your particular setup information. 
 
The sample_env file:
        # .env.example — copy to .env and fill in
        DB_HOST=localhost
        DB_NAME=mlb
        DB_USER=postgres
        DB_PASSWORD=changeme

The database is designed to allow for OLAP analysis of MLB roster transactions. 
The json extracted files are archived as well so data can be added from them for time machine purposes
if such requirements emerge.

MODULE-1: 2026 ROSTER ROOTERS: v0.01

Only the Red Sox and the Active (25) are being tracked in this initial build although the stucture to generalize to other teams is in place. Also, will expand to include the various roster change sizes and include the full 40 person renditions as well at a later point.

The Roster API call:
   statsapi.get('team_roster', {'teamId': team_id=111, 'rosterType': 'active'})

Only retreiving data for team_id = 111 and the "active" roster (25 Person)

The naming convention for the json files is :
  name = f"roster_snapshot_{team_id}_{timestamp}.json"
     So the files look like such: roster_snapshot_111_20260802190349
        111 is team_id 
       2026 is Year
         08 is Month
         02 is Day
         19 is Hour
         03 is Minute
         49 is Second

Thus the files can be pulled at any time and staged for upload. 

This build contains 5 python files and a /sandbox directory with 2 additional python files

/rosters/sandbox:
db_create.py:
  Completely initializes the Postgres database depicted above
  as rosters_snapshots. Eventually place it in a utilities directory.

 roster_play.py:
   Strictly for testing and has some rudemtary and other tests already built.

/
api_get_roster.py:
    calls the API as depicted above and places the .json file into a staging 
    directory /raw_data in the file format depicted above.

roster_loads.py:
    Performs transformations on the .json files and loads the rosters_snapshots database via an upsert 
    of the daily data file and then archives the .json files to the /raw_data/daily_rosters/archive subdirectory.

team_ids.py:
    Lists all the MLB teams and their team_ids

test_files.py:
    A utility to determine if two files are either a duplicate of each other or are 
    unique files. It does this by looking at the size and then the SHA256 Checksum of each file.

.env_example:
    Sample .env file for database credentials. 
    Copy this file and name it .env in your project root directory.
    You will need to place your specific password into this file for your postgres database and change any of the defaults you see in this file
    to match your particular database setup.


NOTABLES:
The routine deduplicate_files(raw_data) in roster_loads.py will remove the duplicates from the staging directory 
(/raw_data/daily_rosters) and leave only unique files.

        def deduplicate_files(raw_data):
            seen = {}    # checksum → first file with that content
            for f in sorted(Path(raw_data).glob('roster_snapshot_*.json')):
                digest = test_files.file_checksum(f)
                if digest in seen:
                    print(f"Duplicate of {seen[digest].name}: {f.name}")
                    os.remove(f)
                else:
                    seen[digest] = f

The main action sequence in roster_loads.py:

        proc_files = deduplicate_files(raw_data)
                for f in proc_files:
                    with open(f, 'r') as file:
                        roster = json.load(file)
                        check_roster(roster)
                        upsert_data(roster)
                archive_files(proc_files)


accesses every unique file in the staging directory (/raw_data/daily_rosters).  It checks the data to be sure it is valid, upserts it and then archives the .json to the archive directory (/raw_data/daily_rosters/archive.

The SQL used for the upsert is: 

 UPSERT_SQL = """
    INSERT INTO roster_snapshots (snapshot_date, team_id, player_id, player_name, position, status) 
    VALUES
        (%(snapshot_date)s, %(team_id)s, %(player_id)s,
        %(player_name)s, %(position)s, %(status)s)
    ON CONFLICT (snapshot_date, team_id, player_id) DO NOTHING;
    """

As can be seen there is a daily grain here that is defaulting to the earliest databse update. 
I will be changing this behavior in a subsequent update to use the latest revision in a day and versionize mutliple updates if they occur in the same day. 
For now, we will keep the current setup as the Daily Grain is important to maintain for later operational use in analysis.











