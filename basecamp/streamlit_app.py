"""Streamlit front end for populating dim_games.

Run from the project root:  streamlit run app/streamlit_app.py

This file collects input and displays results. All the pipeline logic lives in
basecamp/ so the same load can run from cron without Streamlit installed.
"""

from __future__ import annotations

import os
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import dotenv_values, load_dotenv
from psycopg2.extras import RealDictCursor

from basecamp.game_spec import (
    PHASE_BOUNDS,
    PHASE_LABELS,
    SEASON_COLUMN,
    RequestSpec,
    SpecError,
    expand,
)
from basecamp.games_loads import load_files, resolve_mapping, table_meta
from basecamp.games_stage import stage_all

# Anchored to the project root, not to wherever the process happens to start.
# app/streamlit_app.py -> parents[1] is the mlb/ directory.
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)

st.set_page_config(page_title="Populate dim_games", layout="wide")


def conn_kwargs(dbname: str) -> dict:
    """psycopg2.connect() kwargs from the project's DB_* variables.

    Production can override credentials with PROD_DB_USER / PROD_DB_PASSWORD,
    since mlb_dev_user has no CONNECT on mlb. With only DB_* set, both targets
    share one credential pair and the prod attempt fails loudly -- which is the
    point of revoking CONNECT.

    Passing a dict avoids URL-escaping a password into a DSN string.
    """
    prefix = "PROD_" if dbname == "mlb" else ""

    def var(name: str, default: str = "") -> str:
        return os.getenv(f"{prefix}{name}") or os.getenv(name, default)

    return {
        "host": var("DB_HOST", "localhost"),
        "port": var("DB_PORT", "5432"),  # not in .env; container must publish 5432
        "dbname": dbname,
        "user": var("DB_USER"),
        "password": var("DB_PASSWORD"),
    }


# --------------------------------------------------------------------------
# Data the form needs
# --------------------------------------------------------------------------
def query(conn_info: dict, sql: str, params: tuple = ()) -> list[dict]:
    """Read-only helper. closing() is what actually shuts the connection --
    psycopg2's `with conn` only commits or rolls back the transaction."""
    with closing(psycopg2.connect(**conn_info)) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]


@st.cache_data(ttl=600)
def table_columns(conn_info: dict, table: str) -> list[str]:
    rows = query(
        conn_info,
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = current_schema() AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    )
    return [r["column_name"] for r in rows]


def first_present(candidates: list[str], present: list[str]) -> str | None:
    return next((c for c in candidates if c in present), None)


@st.cache_data(ttl=600)
def load_season_bounds(conn_info: dict) -> tuple[dict[int, dict], list[str]]:
    """Returns (bounds keyed by season, boundary columns that don't exist)."""
    present = table_columns(conn_info, "dim_seasons")
    if SEASON_COLUMN not in present:
        raise RuntimeError(
            f"dim_seasons has no {SEASON_COLUMN!r} column. It has: {', '.join(present)}"
        )

    wanted = sorted({c for pair in PHASE_BOUNDS.values() for c in pair})
    usable = [c for c in wanted if c in present]
    missing = [c for c in wanted if c not in present]

    select = ", ".join([SEASON_COLUMN, *usable])
    rows = query(
        conn_info,
        f"SELECT {select} FROM dim_seasons ORDER BY {SEASON_COLUMN} DESC",
    )
    return {int(r[SEASON_COLUMN]): r for r in rows}, missing


@st.cache_data(ttl=600)
def load_teams(conn_info: dict) -> dict[str, int]:
    present = table_columns(conn_info, "dim_teams")
    id_col = first_present(["team_id", "id"], present)
    name_col = first_present(["team_name", "name", "club_name", "full_name"], present)
    if not (id_col and name_col):
        raise RuntimeError(
            f"Can't find id/name columns on dim_teams. It has: {', '.join(present)}"
        )
    rows = query(
        conn_info,
        f"SELECT {id_col} AS team_id, {name_col} AS team_name "
        f"FROM dim_teams ORDER BY {name_col}",
    )
    return {r["team_name"]: r["team_id"] for r in rows}


def existing_counts(conn_info: dict) -> pd.DataFrame:
    rows = query(
        conn_info,
        """
        SELECT season, game_type, count(*) AS games, max(official_date) AS through
        FROM dim_games
        GROUP BY season, game_type
        ORDER BY season DESC, game_type
        """,
    )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Which database
# --------------------------------------------------------------------------
st.title("Populate dim_games")

target = st.sidebar.radio("Database", ["mlb_dev", "mlb (production)"], index=0)
dbname = "mlb_dev" if target.startswith("mlb_dev") else "mlb"
conn_info = conn_kwargs(dbname)
writing_to_prod = dbname == "mlb"

with st.sidebar.expander("Environment"):
    st.write(f"`.env` path: `{ENV_PATH}`")
    st.write("Found on disk" if ENV_PATH.exists() else "**Not found at that path**")
    if ENV_PATH.exists():
        keys = sorted(dotenv_values(ENV_PATH))
        st.write("Keys in file:", ", ".join(keys) or "(none)")
        st.caption(
            f"DB_NAME in .env is `{os.getenv('DB_NAME', '(unset)')}`; the radio "
            "above decides where this app writes."
        )
    st.write("Resolved:", {k: v for k, v in conn_info.items() if k != "password"})
    st.write("Password set" if conn_info["password"] else "**No DB_PASSWORD**")

if not ENV_PATH.exists():
    st.error(f"No .env at {ENV_PATH}. Run streamlit from the project root.")
    st.stop()

if not conn_info["user"]:
    st.error(
        "DB_USER is empty. Check the key names in .env against conn_kwargs() -- "
        "and remember that editing .env needs a full restart, not just a rerun."
    )
    st.stop()

if writing_to_prod:
    st.sidebar.warning("Writes go to production.")
    confirmed = st.sidebar.text_input("Type mlb to unlock") == "mlb"
else:
    confirmed = True

try:
    season_bounds, missing_cols = load_season_bounds(conn_info)
    teams = load_teams(conn_info)
except Exception as exc:  # connection or missing-table problems
    st.error(f"Couldn't read dim_seasons / dim_teams: {exc}")
    st.stop()

if missing_cols:
    st.warning(
        "These boundary columns aren't on dim_seasons, so the phases using them "
        f"are unavailable: {', '.join(missing_cols)}. Map them in PHASE_BOUNDS "
        "(basecamp/game_spec.py) to your real column names."
    )
    with st.expander("Columns dim_seasons actually has"):
        st.write(", ".join(table_columns(conn_info, "dim_seasons")))


# --------------------------------------------------------------------------
# The form: what to pull
# --------------------------------------------------------------------------
left, right = st.columns([2, 3])

with left:
    mode_label = st.radio(
        "Pick games by",
        ["Season and phase", "Date range", "Recent days"],
        help="Season and phase reads its dates from dim_seasons.",
    )
    mode = {"Season and phase": "seasons", "Date range": "range", "Recent days": "recent"}[mode_label]

    phases = st.multiselect(
        "Game types",
        options=list(PHASE_LABELS),
        default=["regular"],
        format_func=lambda p: PHASE_LABELS[p],
    )

    seasons: list[int] = []
    start = end = None
    lookback = 7

    if mode == "seasons":
        seasons = st.multiselect(
            "Seasons",
            options=sorted(season_bounds, reverse=True),
            default=[max(season_bounds)] if season_bounds else [],
        )
    elif mode == "range":
        default_end = date.today()
        picked = st.date_input(
            "Dates",
            value=(default_end - timedelta(days=6), default_end),
        )
        if isinstance(picked, tuple) and len(picked) == 2:
            start, end = picked
    else:
        preset = st.select_slider(
            "Look back",
            options=[1, 3, 7, 14, 30],
            value=7,
            format_func=lambda d: "Yesterday and today" if d == 1 else f"{d} days",
        )
        lookback = preset

    team_name = st.selectbox("Team", ["All teams", *teams], index=0)
    team_id = None if team_name == "All teams" else teams[team_name]

    chunk_days = st.number_input(
        "Days per request", min_value=1, max_value=365, value=30,
        help="Longer ranges are split into this many days per API call and per raw file.",
    )

spec = RequestSpec(
    mode=mode,
    seasons=seasons,
    phases=phases,
    start_date=start,
    end_date=end,
    lookback_days=lookback,
    team_id=team_id,
    chunk_days=int(chunk_days),
)

# --------------------------------------------------------------------------
# Preview
# --------------------------------------------------------------------------
with right:
    st.subheader("Requests this will make")
    try:
        windows = expand(spec, season_bounds)
    except SpecError as exc:
        windows = []
        st.info(str(exc))

    if windows:
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Window": w.label,
                        "Game types": ", ".join(w.game_types),
                        "Days": w.days,
                    }
                    for w in windows
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.caption(f"{len(windows)} API call(s), {sum(w.days for w in windows)} days covered.")

    with st.expander("What's already in dim_games"):
        try:
            st.dataframe(existing_counts(conn_info), hide_index=True, use_container_width=True)
        except Exception as exc:
            st.write(f"Couldn't read dim_games: {exc}")

    with st.expander("How dim_games columns will be mapped"):
        try:
            meta = table_meta(conn_info)
            mapping, unfillable, pk = resolve_mapping(meta)
            st.write("Conflict target:", f"`{pk}`")
            st.write("Filling:", ", ".join(f"`{c}`" for c, _ in mapping))
            skipped = [
                c["column_name"] for c in meta if c["column_name"] not in {m for m, _ in mapping}
            ]
            if skipped:
                st.caption("Left alone: " + ", ".join(skipped))
            if unfillable:
                st.error(
                    "NOT NULL with no default and nothing mapped to them: "
                    + ", ".join(unfillable)
                )
        except Exception as exc:
            st.error(str(exc))

    with st.expander("Spec as JSON (paste this into a cron job)"):
        st.code(spec.to_json(indent=2), language="json")

# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------
st.divider()
staged = st.session_state.setdefault("staged", [])

col_stage, col_load = st.columns(2)

with col_stage:
    if st.button("Fetch and stage", disabled=not windows, type="primary"):
        with st.status("Fetching from the schedule endpoint", expanded=True) as status:
            results = []
            for window in windows:
                st.write(window.label)
                results.extend(stage_all([window]))
            st.session_state["staged"] = [p for p, _ in results]
            total = sum(n for _, n in results)
            status.update(label=f"Staged {total} games in {len(results)} file(s)", state="complete")

with col_load:
    ready = bool(st.session_state["staged"]) and confirmed
    skip_refs = st.checkbox(
        "Skip games with unknown teams/venues",
        help="All-Star squads (159/160) and non-MLB spring opponents aren't in "
             "dim_teams. Leave off to be told which IDs are missing instead.",
    )
    if st.button("Load into dim_games", disabled=not ready):
        result = load_files(
            st.session_state["staged"], conn_info=conn_info, skip_unknown_refs=skip_refs
        )
        st.session_state["staged"] = []
        msg = f"Upserted {result['rows']} rows into dim_games on {target}."
        if result["duplicates"]:
            msg += f" Collapsed {result['duplicates']} repeated gamePk(s)."
        if result["skipped"]:
            msg += f" Skipped {result['skipped']} game(s) with unknown references."
        st.success(msg)
        if result["unknown_refs"]:
            st.info("IDs not in the dimensions: " + "; ".join(
                f"{col}: {', '.join(str(i) for i in ids)}"
                for col, ids in result["unknown_refs"].items()
            ))
        st.cache_data.clear()

if st.session_state["staged"]:
    st.caption("Staged and waiting to load:")
    for path in st.session_state["staged"]:
        st.code(str(path), language=None)
elif not windows:
    st.caption("Pick a season or a date range to get started.")
