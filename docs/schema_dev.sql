--
-- PostgreSQL database dump
--

\restrict 7JxJdQ1Vh35nopATES8JgnwC0Ei4mdezZGuMF0x7dVrpfht7PZmclxp0slDXw1a

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
-- Name: dim_players; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dim_players (
    player_id integer NOT NULL,
    full_name text NOT NULL,
    birth_date date,
    birth_country text,
    birth_city text,
    height text,
    bat_side character(1),
    pitch_hand character(1),
    primary_position text,
    mlb_debut_date date,
    primary_number integer,
    current_age integer,
    loaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: roster_snapshots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roster_snapshots (
    snapshot_date date NOT NULL,
    team_id integer NOT NULL,
    player_id integer NOT NULL,
    player_name character varying(100) NOT NULL,
    "position" character varying(10),
    status character varying(50),
    loaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: dim_players dim_players_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dim_players
    ADD CONSTRAINT dim_players_pkey PRIMARY KEY (player_id);


--
-- Name: roster_snapshots roster_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roster_snapshots
    ADD CONSTRAINT roster_snapshots_pkey PRIMARY KEY (snapshot_date, team_id, player_id);


--
-- PostgreSQL database dump complete
--

\unrestrict 7JxJdQ1Vh35nopATES8JgnwC0Ei4mdezZGuMF0x7dVrpfht7PZmclxp0slDXw1a

