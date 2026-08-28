# db_dates/dates_db.py
import os
import psycopg2
import argparse

import paths  # noqa: F401
from paths import SQL_DIR


def _connect():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
    )


def populate_dim_date(sql_file='sql_popuate_dim_date-2026-1.sql'):
    sql = (SQL_DIR / sql_file).read_text()
    conn = _connect()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql)
            print(f"dim_date: {cur.rowcount} rows inserted")
    finally:
        conn.close()


def apply_season_phases():
    SQL = """
        UPDATE dim_date d SET
            season_phase = CASE
                WHEN d.full_date BETWEEN s.spring_start_date AND s.spring_end_date THEN 'spring'
                WHEN d.full_date BETWEEN s.regular_season_start_date AND s.regular_season_end_date THEN 'regular'
                WHEN d.full_date BETWEEN s.post_season_start_date AND s.post_season_end_date THEN 'postseason'
                ELSE 'offseason'
            END,
            day_of_season = CASE
                WHEN d.full_date BETWEEN s.regular_season_start_date AND s.regular_season_end_date
                THEN (d.full_date - s.regular_season_start_date + 1)
            END
        FROM dim_seasons s
        WHERE s.season = d.season;
    """
    conn = _connect()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(SQL)
            print(f"dim_date: {cur.rowcount} rows updated with season phase")
    finally:
        conn.close()

def main():
    p = argparse.ArgumentParser(description="Populate dim_date")
    p.add_argument('--phases-only', action='store_true',
                   help='Skip generation, just refresh season_phase')
    args = p.parse_args()

    if not args.phases_only:
        populate_dim_date()
    apply_season_phases()
    return 0

if __name__ == "__main__":
    main()