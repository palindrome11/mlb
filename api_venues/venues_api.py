import statsapi
import argparse
from datetime import datetime
import json


def capture_venues(venue_ids):
    ids = ','.join(map(str, venue_ids))
    try:
        return statsapi.get('venue', {
            'venueIds': ids,
            'hydrate': 'location,fieldInfo,timezone'
        })
    except Exception as exc:
        print(f"Venue fetch failed: {type(exc).__name__}: {exc}")
        return None



#API Request DetailsEndpoint 
#URL: https://statsapi.mlb.com/api/v1/venuesMethod: 
#GETAuthentication: None required (free and public)
#Common Query ParameterssportId: Set to 1 for Major League Baseball.
#hydrate: Add extra details like location, fieldInfo, and timezone (comma-separated).

# json{
#   "venues": [
#     {
#       "id": 10,
#       "name": "Dodger Stadium",
#       "link": "/api/v1/venues/10",
#       "location": {
#         "address1": "1000 Vin Scully Avenue",
#         "city": "Los Angeles",
#         "state": "California",
#         "stateAbbrev": "CA",
#         "postalCode": "90012",
#         "country": "USA",
#         "latitude": 34.073964,
#         "longitude": -118.240066
#       },
#       "timeZone": {
#         "id": "America/Los_Angeles",
#         "offset": -7,
#         "tz": "PT"
#       },
#       "fieldInfo": {
#         "capacity": 56000,
#         "turfType": "Grass",
#         "roofType": "Open",
#         "leftLine": 330,
#         "leftCenter": 375,
#         "center": 395,
#         "rightCenter": 375,
#         "rightLine": 330
#       }
#     }
#   ]
# }

def parse_venues(data):
    """Flatten the venue payload into rows for dim_venues."""
    rows = []
    for v in data.get('venues', []):
        loc    = v.get('location') or {}
        coords = loc.get('defaultCoordinates') or {}
        tz     = v.get('timeZone') or {}
        field  = v.get('fieldInfo') or {}

        rows.append({
            'venue_id':      v['id'],
            'name':          v['name'],
            'city':          loc.get('city'),
            'state':         loc.get('state'),
            'state_abbrev':  loc.get('stateAbbrev'),
            'country':       loc.get('country'),
            'postal_code':   loc.get('postalCode'),
            'latitude':      coords.get('latitude'),
            'longitude':     coords.get('longitude'),
            'elevation':     loc.get('elevation'),
            'azimuth_angle': loc.get('azimuthAngle'),
            'time_zone_id':  tz.get('id'),
            'capacity':      field.get('capacity'),
            'turf_type':     field.get('turfType'),
            'roof_type':     field.get('roofType'),
            'left_line':     field.get('leftLine'),
            'left_center':   field.get('leftCenter'),
            'center':        field.get('center'),
            'right_center':  field.get('rightCenter'),
            'right_line':    field.get('rightLine'),
            'active':        v.get('active'),
        })
    return rows




def main():
    parser = argparse.ArgumentParser(description="Please input a venue id to review")
    parser.add_argument("venue_id", type=int, help="Input a venue id for lookup")
    args = parser.parse_args()
    vids = [int(args.venue_id)]
    #print(vids)
    #print(args.venue_id)
    

    venues=capture_venues(vids)
    if venues is None:
        print("Venue fetch failed — nothing loaded -- no such venue identifier")
        exit()

    rows = parse_venues(venues)
    print(f"Parsed {len(rows)} venues")
    for row in rows:
        print(row)

if __name__ == "__main__":
  main()