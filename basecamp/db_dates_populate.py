import paths

from db_dates.db_populate_date_dim import populate_dim_date, apply_season_phases


if __name__ == "__main__":
    populate_dim_date()
    apply_season_phases()
    
