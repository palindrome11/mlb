INSERT INTO dim_date (
    full_date, date_key, year, quarter, month, month_name, month_abbrev,
    day_of_month, day_of_year, day_of_week, day_name, day_abbrev,
    week_of_year, is_weekend, is_month_end, season
)
SELECT
    d::date,
    TO_CHAR(d, 'YYYYMMDD')::INT,
    EXTRACT(YEAR    FROM d),
    EXTRACT(QUARTER FROM d),
    EXTRACT(MONTH   FROM d),
    TRIM(TO_CHAR(d, 'Month')),
    TO_CHAR(d, 'Mon'),
    EXTRACT(DAY     FROM d),
    EXTRACT(DOY     FROM d),
    EXTRACT(DOW     FROM d),
    TRIM(TO_CHAR(d, 'Day')),
    TO_CHAR(d, 'Dy'),
    EXTRACT(WEEK    FROM d),
    EXTRACT(DOW FROM d) IN (0, 6),
    d::date = (DATE_TRUNC('month', d) + INTERVAL '1 month - 1 day')::date,
    EXTRACT(YEAR FROM d)
FROM generate_series('2020-01-01'::date, '2035-12-31'::date, '1 day') AS d
ON CONFLICT (full_date) DO NOTHING;