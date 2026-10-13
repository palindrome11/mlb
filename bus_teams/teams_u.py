from __future__ import annotations
import sys, os 
from datetime import date, datetime
from contextlib import closing
from pathlib import Path
from typing import Any
from psycopg2.extras import RealDictCursor, execute_values
from basecamp.db import connect
import argparse

def get_all_teams(conn):
    SQL_REQUEST="""
    SELECT 
    team_id
    FROM
    dim_teams
    """
    with closing(conn.cursor(cursor_factory=RealDictCursor)) as cursor:
        cursor.execute(SQL_REQUEST)
        return cursor.fetchall()

def get_team_id(team_name, conn):
    SQL_REQUEST="""
    SELECT 
    team_id
    FROM
    dim_teams
    WHERE
    team_name ILIKE %s
    """
    with closing(conn.cursor(cursor_factory=RealDictCursor)) as cursor:
        cursor.execute(SQL_REQUEST, (f"%{team_name}%",))
        result = cursor.fetchone()
        return result['team_id'] if result else None

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")

    parser = argparse.ArgumentParser(description="Specify the team name or id all for name or idretrieval.")
    parser.add_argument('--name', type=str, help=' id, city or name of team (can be a partial match)')
    parser.add_argument("--all", action="store_true", help="process all clubs")
    parser.add_argument('--date', type=date, help='specify a date to get the teams for that year')
     
    args = parser.parse_args()
    team_name = args.name 
    team_date = args.date if args.date else date.today().isoformat()
    team_all = args.all
    
    if team_name:
        print(f"Team Name: {team_name}")
        #game_date=set_game_date('2026-10-08')
        conn = connect()
        team_id = get_team_id(team_name, conn)
        print(team_id)
    elif args.all:
        print("All Team IDs:")
        conn = connect()
        teams = get_all_teams(conn)
        print(f"{len(teams)} Teams")
        #for team in teams:
        #    print(team['team_id'])
        print([team['team_id'] for team in teams])
        return([team['team_id'] for team in teams])
    else:
        print("No team specified. Specify a team using the --name flag or --all for full team id listing")

if __name__ == '__main__':
    main()      
