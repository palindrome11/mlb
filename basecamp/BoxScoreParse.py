"""Flatten a /game/{gamePk}/boxscore payload into fact rows for dim_games.batting and dim_games.pitching."""

from __future__ import annotations

import json
import re
from pathlib import Path

ORDER_RE = re.compile(r"^(\d)(\d)(\d)$")


def load_payload(path: Path) -> dict:
    """Read a staged file, unwrapping the {fetched_at, window, payload} envelope."""
    raw = json.loads(Path(path).read_text())
    return raw.get("payload", raw)


def parse_batting_order(value: str | None) -> tuple[int | None, int | None]:
    """'400' -> (4, 0) fourth in the order, original occupant.
    '501'   -> (5, 1) first substitute at the fifth spot.
    None    -> (None, None) never came to the plate.
    """
    if not value:
        return None, None
    m = ORDER_RE.match(str(value))
    if not m:
        return None, None
    slot, _, sub = m.groups()
    return int(slot), int(sub)


def batting_row(game_pk: int, team_id: int, player: dict) -> tuple | None:
    """One dim_games-linked batting line, or None if the player never batted."""
    b = player.get("stats", {}).get("batting") or {}
    if not b:
        return None

    slot, sub = parse_batting_order(player.get("battingOrder"))
    positions = player.get("allPositions") or []

    return (
        game_pk,
        player["person"]["id"],
        team_id,
        slot,
        sub,
        positions[0]["abbreviation"] if positions else None,
        b.get("plateAppearances", 0),
        b.get("atBats", 0),
        b.get("runs", 0),
        b.get("hits", 0),
        b.get("doubles", 0),
        b.get("triples", 0),
        b.get("homeRuns", 0),
        b.get("rbi", 0),
        b.get("baseOnBalls", 0),
        b.get("intentionalWalks", 0),
        b.get("hitByPitch", 0),
        b.get("strikeOuts", 0),
        b.get("sacBunts", 0),
        b.get("sacFlies", 0),
        b.get("stolenBases", 0),
        b.get("caughtStealing", 0),
        b.get("groundIntoDoublePlay", 0),
        b.get("leftOnBase", 0),
        b.get("totalBases", 0),
    )


def pitching_row(game_pk: int, team_id: int, player: dict) -> tuple | None:
    """One pitching line, or None if the player never pitched."""
    p = player.get("stats", {}).get("pitching") or {}
    if not p:
        return None

    return (
        game_pk,
        player["person"]["id"],
        team_id,
        p.get("gamesStarted", 0) == 1,
        p.get("outs", 0),            # integer -- ignore inningsPitched "3.1"
        p.get("battersFaced", 0),
        p.get("hits", 0),
        p.get("runs", 0),
        p.get("earnedRuns", 0),
        p.get("homeRuns", 0),
        p.get("baseOnBalls", 0),
        p.get("intentionalWalks", 0),
        p.get("hitBatsmen", 0),
        p.get("strikeOuts", 0),
        p.get("wildPitches", 0),
        p.get("balks", 0),
        p.get("pitchesThrown", 0),
        p.get("strikes", 0),
        p.get("inheritedRunners", 0),
        p.get("inheritedRunnersScored", 0),
        p.get("wins", 0) == 1,
        p.get("losses", 0) == 1,
        p.get("saves", 0) == 1,
        p.get("holds", 0),
        p.get("blownSaves", 0),
    )


def parse_game(payload: dict, game_pk: int) -> dict:
    """-> {"batting": [rows], "pitching": [rows]} across both teams."""
    batting, pitching = [], []

    for side in ("away", "home"):
        team = payload["teams"][side]
        team_id = team["team"]["id"]

        for player in team.get("players", {}).values():
            if (row := batting_row(game_pk, team_id, player)) is not None:
                batting.append(row)
            if (row := pitching_row(game_pk, team_id, player)) is not None:
                pitching.append(row)

    return {"batting": batting, "pitching": pitching}


def check_totals(payload: dict, parsed: dict) -> list[str]:
    """Compare parsed player rows against the payload's own team totals.

    Only counting stats -- teamStats rate fields (avg, era) are season figures
    mixed into a game-level object, so they can't be validated this way.
    """
    problems = []
    # column offsets into the tuples above
    AB, HITS, RUNS = 7, 9, 8

    for side in ("away", "home"):
        team = payload["teams"][side]
        team_id = team["team"]["id"]
        totals = team.get("teamStats", {}).get("batting", {})
        rows = [r for r in parsed["batting"] if r[2] == team_id]

        for label, idx, key in (("AB", AB, "atBats"), ("H", HITS, "hits"), ("R", RUNS, "runs")):
            got, want = sum(r[idx] for r in rows), totals.get(key)
            if want is not None and got != want:
                problems.append(f"{side} {label}: rows sum to {got}, teamStats says {want}")

    return problems


if __name__ == "__main__":
    import sys

    payload = load_payload(sys.argv[1])
    parsed = parse_game(payload, game_pk=int(sys.argv[2]))
    print(f"batting rows: {len(parsed['batting'])}")
    print(f"pitching rows: {len(parsed['pitching'])}")
    for problem in check_totals(payload, parsed):
        print("MISMATCH:", problem)