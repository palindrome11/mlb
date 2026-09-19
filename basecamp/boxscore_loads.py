"""Load boxscore payloads from boxscore_raw into the fact tables.


Usage:
    python -m basecamp.boxscore_loads 813000 813001
    python -m basecamp.boxscore_loads --game_ids 813000,813001
    python -m basecamp.boxscore_loads --all
    python -m basecamp.boxscore_loads --all --dry-run
    python -m basecamp.boxscore_loads --all --keep-raw
"""

from __future__ import annotations

import argparse
import json
import sys
from contextlib import closing

from psycopg2.extras import execute_values

from basecamp.BoxScoreParse import check_totals, parse_game
from basecamp.db import connect

BATTING_COLUMNS = [
    "game_pk", "player_id", "team_id", "batting_order", "batting_sub_index",
    "position", "plate_appearances", "at_bats", "runs", "hits", "doubles",
    "triples", "home_runs", "rbi", "walks", "intentional_walks", "hit_by_pitch",
    "strikeouts", "sac_bunts", "sac_flies", "stolen_bases", "caught_stealing",
    "gidp", "left_on_base", "total_bases",
]

PITCHING_COLUMNS = [
    "game_pk", "player_id", "team_id", "is_starter", "outs_recorded",
    "batters_faced", "hits", "runs", "earned_runs", "home_runs", "walks",
    "intentional_walks", "hit_batsmen", "strikeouts", "wild_pitches", "balks",
    "pitches_thrown", "strikes", "inherited_runners", "inherited_runners_scored",
    "is_win", "is_loss", "is_save", "holds", "blown_saves",
]


def build_upsert(table: str, columns: list[str]) -> str:
    """Upsert keyed on (game_pk, player_id) -- games do get rescored."""
    updates = [f"{c} = EXCLUDED.{c}" for c in columns if c not in ("game_pk", "player_id")]
    return f"""
        INSERT INTO {table} ({", ".join(columns)})
        VALUES %s
        ON CONFLICT (game_pk, player_id) DO UPDATE SET
            {", ".join(updates)},
            loaded_at = now()
    """


BATTING_UPSERT = build_upsert("fact_batting", BATTING_COLUMNS)
PITCHING_UPSERT = build_upsert("fact_pitching", PITCHING_COLUMNS)

SELECT_PENDING = """
    SELECT r.game_pk
    FROM boxscore_raw r
    JOIN dim_games g USING (game_pk)
    WHERE g.coded_game_state = 'F'
    ORDER BY r.game_pk
"""

SELECT_PAYLOAD = "SELECT payload FROM boxscore_raw WHERE game_pk = %s"
DELETE_RAW = "DELETE FROM boxscore_raw WHERE game_pk = %s"


def as_dict(payload) -> dict:
    """jsonb comes back as a dict, text comes back as a string."""
    return payload if isinstance(payload, dict) else json.loads(payload)


def pending_game_ids(conn) -> list[int]:
    """Raw payloads for games that are final and therefore safe to load."""
    with conn.cursor() as cur:
        cur.execute(SELECT_PENDING)
        return [r[0] for r in cur.fetchall()]


def load_game(conn, game_pk: int, keep_raw: bool = False, dry_run: bool = False) -> dict:
    """Parse and load one game. Returns counts plus any total mismatches.

    One transaction per game: the two upserts and the delete commit together,
    so an interrupted backfill leaves no half-loaded game and no orphaned
    buffer row. Restart picks up where it stopped.
    """
    with conn.cursor() as cur:
        cur.execute(SELECT_PAYLOAD, (game_pk,))
        row = cur.fetchone()

    if row is None:
        return {"game_pk": game_pk, "status": "not found", "batting": 0, "pitching": 0}

    payload = as_dict(row[0])
    parsed = parse_game(payload, game_pk)
    problems = check_totals(payload, parsed)

    result = {
        "game_pk": game_pk,
        "status": "ok",
        "batting": len(parsed["batting"]),
        "pitching": len(parsed["pitching"]),
        "problems": problems,
    }

    if dry_run:
        result["status"] = "dry run"
        return result

    if problems:
        # The payload disagrees with itself -- don't write, don't delete.
        result["status"] = "totals mismatch, skipped"
        return result

    with conn, conn.cursor() as cur:
        if parsed["batting"]:
            execute_values(cur, BATTING_UPSERT, parsed["batting"], page_size=500)
        if parsed["pitching"]:
            execute_values(cur, PITCHING_UPSERT, parsed["pitching"], page_size=500)
        if not keep_raw:
            cur.execute(DELETE_RAW, (game_pk,))

    return result


def comma_separated_integers(value: str) -> list[int]:
    try:
        return [int(v) for v in value.split(",") if v.strip()]
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected comma-separated integers, got {value!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Load boxscores from boxscore_raw into the fact tables.")
    parser.add_argument("ids", nargs="*", type=int, metavar="GAME_PK",
                        help="Game ids as positional arguments")
    parser.add_argument("--game_ids", type=comma_separated_integers, default=[],
                        help="Comma-separated game ids (e.g. 813000,813001)")
    parser.add_argument("--all", action="store_true",
                        help="Load every staged payload whose game is Final")
    parser.add_argument("--keep-raw", action="store_true",
                        help="Don't delete the payload after loading")
    parser.add_argument("--dry-run", action="store_true",
                        help="Parse and validate, write nothing")
    args = parser.parse_args()

    with closing(connect()) as conn:
        game_ids = args.ids + args.game_ids
        if args.all:
            game_ids += pending_game_ids(conn)
        if not game_ids:
            parser.error("give game ids positionally, with --game_ids, or use --all")

        totals = {"batting": 0, "pitching": 0, "failed": 0}

        for game_pk in dict.fromkeys(game_ids):   # de-dupe, keep order
            result = load_game(conn, game_pk, keep_raw=args.keep_raw, dry_run=args.dry_run)
            totals["batting"] += result["batting"]
            totals["pitching"] += result["pitching"]

            line = f"{game_pk}: {result['batting']} batting, {result['pitching']} pitching"
            if result["status"] != "ok":
                totals["failed"] += 1
                line += f"  [{result['status']}]"
            print(line)

            for problem in result.get("problems", []):
                print(f"    {problem}", file=sys.stderr)

        print(f"\n{totals['batting']} batting rows, {totals['pitching']} pitching rows, "
              f"{totals['failed']} game(s) not loaded")

    return 1 if totals["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
