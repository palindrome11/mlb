"""Load: flatten staged schedule JSON into dim_games, then deletethe file.
 
Rather than hardcode column names, this resolves each API field against the
columns dim_games actually has. Add an alias to FIELDS if your name isn't
listed; the INSERT is built from whatever resolves.
"""
 
from __future__ import annotations
 
import json
import shutil
from contextlib import closing
from pathlib import Path
 
from psycopg2.extras import RealDictCursor, execute_values
 
from basecamp.db import connect
from basecamp.games_stage import RAW_DIR
 
ARCHIVE_DIR = RAW_DIR / "archive"


# (candidate column names, how to pull the value out of one API game object)
# First candidate present in the table wins.
FIELDS: list[tuple[list[str], callable]] = [
    (["game_pk", "gamepk", "game_id"], lambda g: g["gamePk"]),
    (["season", "season_id", "season_year"], lambda g: int(g["season"])),
    (["game_type", "gametype", "game_type_code"], lambda g: g["gameType"]),
    (["official_date", "game_date", "date"], lambda g: g["officialDate"]),
    (
        ["game_datetime_utc", "game_datetime", "game_date_utc", "game_timestamp", "game_time"],
        lambda g: g["gameDate"],  # ISO 8601 UTC
    ),
    (["home_team_id", "home_id"], lambda g: g["teams"]["home"]["team"]["id"]),
    (["away_team_id", "away_id"], lambda g: g["teams"]["away"]["team"]["id"]),
    (["venue_id"], lambda g: (g.get("venue") or {}).get("id")),
    (
        ["coded_game_state","status_detailed", "detailed_state", "game_status", "status"],
        lambda g: g["status"]["codedGameState"],
    ),
    (["day_night", "daynight"], lambda g: g.get("dayNight")),
    (["doubleheader", "double_header"], lambda g: g.get("doubleHeader")),
    (["game_number", "game_num"], lambda g: g.get("gameNumber")),
    (["series_description", "series_desc"], lambda g: g.get("seriesDescription")),
    (["resumed_from"], lambda g: g.get("resumeDate")),
    (["rescheduled_from"], lambda g: g.get("rescheduledFrom")),    
]
 
PK_CANDIDATES = ["game_pk", "gamepk", "game_id"]
TIMESTAMP_CANDIDATES = ["loaded_at", "updated_at", "load_ts"]
 
 
class SchemaMismatch(RuntimeError):
    """dim_games can't be populated with the fields available."""
 
 
class UnknownReference(RuntimeError):
    """Rows reference dimension members that don't exist yet."""
 
 
# (candidate columns on dim_games, dimension table, candidate key columns there)
REFERENCES = [
    (["home_team_id", "home_id"], "dim_teams", ["team_id", "id"]),
    (["away_team_id", "away_id"], "dim_teams", ["team_id", "id"]),
    (["venue_id"], "dim_venues", ["venue_id", "id"]),
]
 
 
def table_meta(conn_info=None, table: str = "dim_games") -> list[dict]:
    """Column name, nullability and default, straight from the catalog."""
    sql = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = current_schema() AND table_name = %s
        ORDER BY ordinal_position
    """
    with closing(connect(conn_info)) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (table,))
            return [dict(r) for r in cur.fetchall()]
 
 
def resolve_mapping(meta: list[dict]) -> tuple[list[tuple[str, callable]], list[str], str]:
    """Match FIELDS against real columns.
 
    Returns (mapping, unfillable_required_columns, pk_column).
    """
    present = [c["column_name"] for c in meta]
    if not present:
        raise SchemaMismatch("dim_games not found in the current schema.")
 
    mapping: list[tuple[str, callable]] = []
    for candidates, extractor in FIELDS:
        col = next((c for c in candidates if c in present), None)
        if col:
            mapping.append((col, extractor))
 
    mapped = {col for col, _ in mapping}
 
    pk = next((c for c in PK_CANDIDATES if c in mapped), None)
    if not pk:
        raise SchemaMismatch(
            "No game_pk-style column on dim_games to conflict on. "
            f"Columns: {', '.join(present)}"
        )
 
    # NOT NULL, no default, and nothing to put in it -> the INSERT will fail.
    unfillable = [
        c["column_name"]
        for c in meta
        if c["is_nullable"] == "NO"
        and not c["column_default"]
        and c["column_name"] not in mapped
    ]
    return mapping, unfillable, pk
 
 
def build_upsert(mapping, pk: str, present: list[str]) -> str:
    cols = [c for c, _ in mapping]
    sets = [f"{c} = EXCLUDED.{c}" for c in cols if c != pk]
    stamp = next((c for c in TIMESTAMP_CANDIDATES if c in present), None)
    if stamp:
        sets.append(f"{stamp} = now()")
    return f"""
        INSERT INTO dim_games ({", ".join(cols)})
        VALUES %s
        ON CONFLICT ({pk}) DO UPDATE SET
            {", ".join(sets)}
    """
 
 
def rows_from_file(path: Path, mapping) -> list[tuple]:
    envelope = json.loads(Path(path).read_text())
    payload = envelope.get("payload", envelope)
    games = [g for day in payload.get("dates", []) for g in day.get("games", [])]
    return [tuple(extract(g) for _, extract in mapping) for g in games]
 
 
def _columns(conn, table: str) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = current_schema() AND table_name = %s
            ORDER BY ordinal_position
            """,
            (table,),
        )
        return [r[0] for r in cur.fetchall()]
 
 
def check_references(conn, mapping, rows) -> dict[str, set]:
    """Which referenced IDs are missing from the dimensions, per dim_games column."""
    cols = [c for c, _ in mapping]
    missing: dict[str, set] = {}
 
    for candidates, ref_table, ref_keys in REFERENCES:
        col = next((c for c in candidates if c in cols), None)
        if not col:
            continue
        ref_cols = _columns(conn, ref_table)
        if not ref_cols:  # dimension doesn't exist; nothing to enforce
            continue
        ref_key = next((k for k in ref_keys if k in ref_cols), None)
        if not ref_key:
            continue
 
        used = {row[cols.index(col)] for row in rows if row[cols.index(col)] is not None}
        if not used:
            continue
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT {ref_key} FROM {ref_table} WHERE {ref_key} = ANY(%s)",
                (list(used),),
            )
            known = {r[0] for r in cur.fetchall()}
        absent = used - known
        if absent:
            missing[col] = absent
 
    return missing
 
 
def _drop_unknown(mapping, rows, missing: dict[str, set]) -> list[tuple]:
    cols = [c for c, _ in mapping]
    keep = []
    for row in rows:
        if any(row[cols.index(col)] in bad for col, bad in missing.items()):
            continue
        keep.append(row)
    return keep
 
 
def dedupe(rows: list[tuple], pk_index: int) -> tuple[list[tuple], int]:
    """Collapse repeated conflict keys within one batch.
 
    Postgres refuses to let ON CONFLICT DO UPDATE hit the same row twice in a
    single command. The schedule feed legitimately repeats a gamePk -- suspended
    games appear under both the original and the resume date, likewise for
    reschedules -- so keep the last occurrence, which carries the newer status.
    """
    seen: dict = {}
    for row in rows:
        seen[row[pk_index]] = row
    return list(seen.values()), len(rows) - len(seen)
 
 
def load_files(
    paths: list[Path],
    conn_info: dict | str | None = None,
    on_success: str = "delete",
    skip_unknown_refs: bool = False,
) -> dict:
    """Upsert staged files. Resolves the schema once, then loads each file.
 
    Games referencing teams or venues that aren't in the dimensions are either
    reported (default) or skipped. All-Star squads are teamIds 159 and 160;
    spring games against college or WBC opponents use other non-club IDs.
    """
    meta = table_meta(conn_info)
    mapping, unfillable, pk = resolve_mapping(meta)
    if unfillable:
        raise SchemaMismatch(
            "These dim_games columns are NOT NULL with no default and nothing "
            f"maps to them: {', '.join(unfillable)}. Add an entry to FIELDS or "
            "give the column a default."
        )
 
    present = [c["column_name"] for c in meta]
    sql = build_upsert(mapping, pk, present)
    pk_index = [c for c, _ in mapping].index(pk)
    per_file: dict[str, int] = {}
    duplicates = 0
    skipped = 0
    unknown: dict[str, set] = {}
 
    with closing(connect(conn_info)) as conn:
        for path in paths:
            rows, dropped = dedupe(rows_from_file(path, mapping), pk_index)
            duplicates += dropped
 
            missing = check_references(conn, mapping, rows)
            if missing:
                for col, ids in missing.items():
                    unknown.setdefault(col, set()).update(ids)
                if not skip_unknown_refs:
                    detail = "; ".join(
                        f"{col}: {', '.join(str(i) for i in sorted(ids))}"
                        for col, ids in sorted(missing.items())
                    )
                    raise UnknownReference(
                        f"{Path(path).name} references IDs that aren't in the "
                        f"dimensions -- {detail}. Load those dimension rows first, "
                        "or re-run with skip_unknown_refs=True."
                    )
                before = len(rows)
                rows = _drop_unknown(mapping, rows, missing)
                skipped += before - len(rows)
 
            if rows:
                # `with conn` commits per file, so one bad file doesn't
                # roll back the ones already loaded.
                with conn, conn.cursor() as cur:
                    execute_values(cur, sql, rows, page_size=500)
            per_file[str(path)] = len(rows)
 
            if rows:
                if on_success == "archive":
                    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), ARCHIVE_DIR / Path(path).name)
                elif on_success == "delete":
                    Path(path).unlink(missing_ok=True)
            

    return {
        "files": per_file,
        "rows": sum(per_file.values()),
        "duplicates": duplicates,
        "skipped": skipped,
        "unknown_refs": {c: sorted(v) for c, v in unknown.items()},
        "columns": [c for c, _ in mapping],
    }

def load_file(path: Path, conn_info=None, on_success: str = "delete") -> int:
    return load_files([path], conn_info, on_success)["rows"] 
 
