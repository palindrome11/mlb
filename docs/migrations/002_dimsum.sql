--
-- PostgreSQL database dump
--

\restrict LVvEroehK4g91wamP4WUemRpHXjCqtExnmSbO2WxbWF2BPbaeL59yoZdnHeBOHb

-- Dumped from database version 18.4 (Debian 18.4-1.pgdg13+1)
-- Dumped by pg_dump version 18.4 (Debian 18.4-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: roster_snapshots; Type: TABLE; Schema: public; Owner: -
--

ALTER TABLE public.roster_snapshots
    ADD COLUMN IF NOT EXISTS version    integer     NOT NULL DEFAULT 1,
    ADD COLUMN IF NOT EXISTS updated_at timestamptz NOT NULL DEFAULT now();
UPDATE public.roster_snapshots
SET updated_at = loaded_at
WHERE updated_at <> loaded_at;

--
-- Name: boxscore_raw; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.boxscore_raw (
    game_pk integer NOT NULL,
    fetched_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    payload jsonb NOT NULL
);

--
-- Name: dim_date; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dim_date (
    full_date date NOT NULL,
    date_key integer NOT NULL,
    year smallint NOT NULL,
    quarter smallint NOT NULL,
    month smallint NOT NULL,
    month_name text NOT NULL,
    month_abbrev character(3) NOT NULL,
    day_of_month smallint NOT NULL,
    day_of_year smallint NOT NULL,
    day_of_week smallint NOT NULL,
    day_name text NOT NULL,
    day_abbrev character(3) NOT NULL,
    week_of_year smallint NOT NULL,
    is_weekend boolean NOT NULL,
    is_month_end boolean NOT NULL,
    season smallint,
    season_phase text,
    day_of_season smallint
);


--
-- Name: dim_games; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dim_games (
    game_pk integer NOT NULL,
    official_date date NOT NULL,
    game_datetime timestamp with time zone,
    season smallint,
    game_type character(1),
    home_team_id integer,
    away_team_id integer,
    venue_id integer,
    game_number smallint,
    doubleheader character(1),
    day_night text,
    coded_game_state character(1),
    resumed_from date,
    rescheduled_from date,
    loaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: dim_seasons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dim_seasons (
    season smallint NOT NULL,
    pre_season_start_date date,
    spring_start_date date,
    spring_end_date date,
    regular_season_start_date date,
    last_date_1st_half date,
    all_star_date date,
    first_date_2nd_half date,
    regular_season_end_date date,
    post_season_start_date date,
    post_season_end_date date,
    offseason_start_date date,
    loaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: dim_teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dim_teams (
    team_id integer NOT NULL,
    name text NOT NULL,
    team_code text,
    abbreviation text,
    club_name text,
    location_name text,
    league_id integer,
    league_name text,
    division_id integer,
    division_name text,
    venue_id integer,
    venue_name text,
    first_year text,
    active boolean,
    loaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: dim_venues; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dim_venues (
    venue_id integer NOT NULL,
    name text NOT NULL,
    city text,
    state text,
    state_abbrev character(2),
    country text,
    postal_code text,
    latitude numeric(10,7),
    longitude numeric(10,7),
    elevation integer,
    azimuth_angle numeric(5,2),
    time_zone_id text,
    capacity integer,
    turf_type text,
    roof_type text,
    left_line integer,
    left_center integer,
    center integer,
    right_center integer,
    right_line integer,
    active boolean,
    loaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: fact_batting; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fact_batting (
    game_pk integer NOT NULL,
    player_id integer NOT NULL,
    team_id integer NOT NULL,
    is_starter boolean,
    outs smallint,
    batters_faced smallint,
    pitches smallint,
    strikes smallint,
    hits smallint,
    runs smallint,
    earned_runs smallint,
    home_runs smallint,
    walks smallint,
    intentional_walks smallint,
    strikeouts smallint,
    hit_batsmen smallint,
    wild_pitches smallint,
    balks smallint,
    inherited_runners smallint,
    inherited_runners_scored smallint,
    decision character(1),
    loaded_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: fact_pitching; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fact_pitching (
    game_pk integer NOT NULL,
    player_id integer NOT NULL,
    team_id integer NOT NULL,
    is_starter boolean,
    outs smallint,
    batters_faced smallint,
    pitches smallint,
    strikes smallint,
    hits smallint,
    runs smallint,
    earned_runs smallint,
    home_runs smallint,
    walks smallint,
    intentional_walks smallint,
    strikeouts smallint,
    hit_batsmen smallint,
    wild_pitches smallint,
    balks smallint,
    inherited_runners smallint,
    inherited_runners_scored smallint,
    decision character(1),
    loaded_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: boxscore_raw boxscore_raw_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.boxscore_raw
    ADD CONSTRAINT boxscore_raw_pkey PRIMARY KEY (game_pk);


--
-- Name: dim_date dim_date_date_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_date_key_key UNIQUE (date_key);


--
-- Name: dim_date dim_date_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (full_date);


--
-- Name: dim_games dim_games_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_games
    ADD CONSTRAINT dim_games_pkey PRIMARY KEY (game_pk);


--
-- Name: dim_seasons dim_seasons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_seasons
    ADD CONSTRAINT dim_seasons_pkey PRIMARY KEY (season);


--
-- Name: dim_teams dim_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_teams
    ADD CONSTRAINT dim_teams_pkey PRIMARY KEY (team_id);


--
-- Name: dim_venues dim_venues_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_venues
    ADD CONSTRAINT dim_venues_pkey PRIMARY KEY (venue_id);


--
-- Name: fact_batting fact_batting_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_batting
    ADD CONSTRAINT fact_batting_pkey PRIMARY KEY (game_pk, player_id);


--
-- Name: fact_pitching fact_pitching_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_pitching
    ADD CONSTRAINT fact_pitching_pkey PRIMARY KEY (game_pk, player_id);


--
-- Name: dim_games dim_games_away_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_games
    ADD CONSTRAINT dim_games_away_team_id_fkey FOREIGN KEY (away_team_id) REFERENCES public.dim_teams(team_id);


--
-- Name: dim_games dim_games_home_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_games
    ADD CONSTRAINT dim_games_home_team_id_fkey FOREIGN KEY (home_team_id) REFERENCES public.dim_teams(team_id);


--
-- Name: fact_batting fact_batting_game_pk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_batting
    ADD CONSTRAINT fact_batting_game_pk_fkey FOREIGN KEY (game_pk) REFERENCES public.dim_games(game_pk);


--
-- Name: fact_batting fact_batting_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_batting
    ADD CONSTRAINT fact_batting_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.dim_players(player_id);


--
-- Name: fact_batting fact_batting_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_batting
    ADD CONSTRAINT fact_batting_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.dim_teams(team_id);


--
-- Name: fact_pitching fact_pitching_game_pk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_pitching
    ADD CONSTRAINT fact_pitching_game_pk_fkey FOREIGN KEY (game_pk) REFERENCES public.dim_games(game_pk);


--
-- Name: fact_pitching fact_pitching_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_pitching
    ADD CONSTRAINT fact_pitching_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.dim_players(player_id);


--
-- Name: fact_pitching fact_pitching_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_pitching
    ADD CONSTRAINT fact_pitching_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.dim_teams(team_id);


--
-- PostgreSQL database dump complete
--

\unrestrict LVvEroehK4g91wamP4WUemRpHXjCqtExnmSbO2WxbWF2BPbaeL59yoZdnHeBOHb

