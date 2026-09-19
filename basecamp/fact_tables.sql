-- Fact tables for per-game hitting and pitching lines.
--
-- Counting stats only. Every column here is additive, so summing across any
-- slice gives a correct answer. Rates (AVG, ERA, WHIP, OPS) are computed in
-- views -- see the bottom of this file.
--
-- Separate tables because the measure sets don't overlap and a two-way player
-- legitimately appears in both for the same game.

CREATE TABLE IF NOT EXISTS fact_batting (
    game_pk             integer NOT NULL REFERENCES dim_games(game_pk),
    player_id           integer NOT NULL,
    team_id             integer NOT NULL REFERENCES dim_teams(team_id),
    batting_order       smallint,          -- 1-9, NULL if never batted
    batting_sub_index   smallint,          -- 0 = original occupant of the slot
    position            text,
    plate_appearances   smallint NOT NULL DEFAULT 0,
    at_bats             smallint NOT NULL DEFAULT 0,
    runs                smallint NOT NULL DEFAULT 0,
    hits                smallint NOT NULL DEFAULT 0,
    doubles             smallint NOT NULL DEFAULT 0,
    triples             smallint NOT NULL DEFAULT 0,
    home_runs           smallint NOT NULL DEFAULT 0,
    rbi                 smallint NOT NULL DEFAULT 0,
    walks               smallint NOT NULL DEFAULT 0,
    intentional_walks   smallint NOT NULL DEFAULT 0,
    hit_by_pitch        smallint NOT NULL DEFAULT 0,
    strikeouts          smallint NOT NULL DEFAULT 0,
    sac_bunts           smallint NOT NULL DEFAULT 0,
    sac_flies           smallint NOT NULL DEFAULT 0,
    stolen_bases        smallint NOT NULL DEFAULT 0,
    caught_stealing     smallint NOT NULL DEFAULT 0,
    gidp                smallint NOT NULL DEFAULT 0,
    left_on_base        smallint NOT NULL DEFAULT 0,
    total_bases         smallint NOT NULL DEFAULT 0,
    loaded_at           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (game_pk, player_id)
);

CREATE INDEX IF NOT EXISTS fact_batting_player_idx ON fact_batting (player_id);
CREATE INDEX IF NOT EXISTS fact_batting_team_idx   ON fact_batting (team_id);

CREATE TABLE IF NOT EXISTS fact_pitching (
    game_pk                  integer NOT NULL REFERENCES dim_games(game_pk),
    player_id                integer NOT NULL,
    team_id                  integer NOT NULL REFERENCES dim_teams(team_id),
    is_starter               boolean NOT NULL DEFAULT false,
    outs_recorded            smallint NOT NULL DEFAULT 0,  -- 19 = 6.1 IP
    batters_faced            smallint NOT NULL DEFAULT 0,
    hits                     smallint NOT NULL DEFAULT 0,
    runs                     smallint NOT NULL DEFAULT 0,
    earned_runs              smallint NOT NULL DEFAULT 0,
    home_runs                smallint NOT NULL DEFAULT 0,
    walks                    smallint NOT NULL DEFAULT 0,
    intentional_walks        smallint NOT NULL DEFAULT 0,
    hit_batsmen              smallint NOT NULL DEFAULT 0,
    strikeouts               smallint NOT NULL DEFAULT 0,
    wild_pitches             smallint NOT NULL DEFAULT 0,
    balks                    smallint NOT NULL DEFAULT 0,
    pitches_thrown           smallint NOT NULL DEFAULT 0,
    strikes                  smallint NOT NULL DEFAULT 0,
    inherited_runners        smallint NOT NULL DEFAULT 0,
    inherited_runners_scored smallint NOT NULL DEFAULT 0,
    is_win                   boolean NOT NULL DEFAULT false,
    is_loss                  boolean NOT NULL DEFAULT false,
    is_save                  boolean NOT NULL DEFAULT false,
    holds                    smallint NOT NULL DEFAULT 0,
    blown_saves              smallint NOT NULL DEFAULT 0,
    loaded_at                timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (game_pk, player_id)
);

CREATE INDEX IF NOT EXISTS fact_pitching_player_idx ON fact_pitching (player_id);
CREATE INDEX IF NOT EXISTS fact_pitching_team_idx   ON fact_pitching (team_id);


-- Rates computed at query time. NULLIF guards the zero-denominator case,
-- which returns NULL rather than raising.

CREATE OR REPLACE VIEW v_batting_rates AS
SELECT game_pk, player_id, team_id,
       hits::numeric / NULLIF(at_bats, 0)                             AS avg,
       (hits + walks + hit_by_pitch)::numeric
           / NULLIF(at_bats + walks + hit_by_pitch + sac_flies, 0)     AS obp,
       total_bases::numeric / NULLIF(at_bats, 0)                       AS slg
FROM fact_batting;

CREATE OR REPLACE VIEW v_pitching_rates AS
SELECT game_pk, player_id, team_id,
       outs_recorded / 3 || '.' || outs_recorded % 3                   AS innings_pitched,
       earned_runs * 27.0 / NULLIF(outs_recorded, 0)                   AS era,
       (walks + hits) * 3.0 / NULLIF(outs_recorded, 0)                 AS whip
FROM fact_pitching;
