## Interpreting and Parsing the API Endpoints JSON Return Payloads

1. Look at it in a browser
	Paste the raw URL into Chrome or Firefox:
	<https://statsapi.mlb.com/api/v1/teams/111/roster?rosterType=active>
	Firefox has a built-in collapsible JSON viewer. 
	In Chrome, tick “Pretty-print”. 
	
	This is the fastest way to get a feel for the structure.

2. Dump it from Python

python
import json, statsapi

data = statsapi.get("team_roster", {"teamId": 111})
print(json.dumps(data, indent=2)[:3000])    # first chunk
print(data.keys())                           # top-level keys
print(data["roster"][0].keys())              # keys of one item

You already save raw JSON to raw_data/, so those files are a ready-made reference library. Open one in VS Code and collapse or expand the sections.

3. Explore with jq in the terminal
bash
brew install jq
jq 'keys' roster.json                    # top-level keys
jq '.roster[0]' roster.json              # one full record
jq '[paths | map(tostring) | join(".")]' roster.json | sort -u   # every field path

The last command lists every field path in the file, which is very useful for planning table columns.

4. Generate a schema automatically
bash
pip install genson
genson roster.json > roster_schema.json

This infers a JSON Schema with field names, types, and nesting from a real response. Run it on several responses and merge them, because optional fields don’t always appear.
