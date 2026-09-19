import paths
import argparse


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

def add_individual_venues(venue_ids):
    if len(venue_ids) >= 1:
        print(f"Processing {len(venue_ids)} venues")
        venue_info=capture_venues(venue_ids)
        venues=capture_venues(venue_ids)
        venue_info_rows=parse_venues(venues)
        print(venue_info_rows)
        #for row in venue_info_rows:
        #    print(len(venue_info_rows))
        #    print(row)   
        upsert_venues_data(venue_info_rows)
    else:
        print("\n *** No new venues to add from the active games / teams tables *** \n")

def main():
    parser = argparse.ArgumentParser(
        description="Add venue information to the database. You can specify individual venue IDs or use the --active-venue-ids flag to add all active venues."
    )   
    parser.add_argument("--venue-ids", nargs="+", help="List of venue IDs to add")
    parser.add_argument("--active-venue-ids", nargs="+", help="List of active venue IDs to add")
    args = parser.parse_args()

    if args.venue_ids:  
        add_individual_venues(args.venue_ids)
    elif args.active_venue_ids:
        add_active_venues(args.active_venue_ids)
    else:
       print("No venue IDs provided. Please use --venue-ids or --active-venue-ids to specify venue IDs.")

if __name__ == '__main__':
    main()
