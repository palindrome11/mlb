import paths

from bus_venues.venue_id_search import get_missing_venue_ids
from api_venues.venues_api import capture_venues, parse_venues
from db_venues.venues_db import upsert_venues_data

def add_active_venues():
    venue_ids=get_missing_venue_ids()
    if len(venue_ids) >= 1:
        print(f"Processing {len(venue_ids)} venues")
        venue_info=capture_venues(venue_ids)
        venues=capture_venues(venue_ids)
        venue_info_rows=parse_venues(venues)
        #for row in venue_info_rows:
        #    print(len(venue_info_rows))
        #    print(row)   
        upsert_venues_data(venue_info_rows)
    else:
        print("\n *** No new venues to add from the active games / teams tables *** \n")

def main():
    add_active_venues()
    

if __name__ == '__main__':
    main()
