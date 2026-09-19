"""Extract: turn Windows into raw schedule JSON files on disk.

Mirrors rosters_stage.py -- this module only writes raw payloads, it never
touches Postgres. Nothing here imports Streamlit.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import statsapi

from basecamp.game_spec import Window

RAW_DIR = Path(os.getenv("RAW_DATA_DIR", "raw_data")) / "games"


def fetch(window: Window) -> dict:
    """Hit /api/v1/schedule for one window.

    statsapi.schedule() flattens the response and doesn't expose gameType, so
    call the raw endpoint through statsapi.get() instead.
    """
    params = {
        "sportId": 1,
        "startDate": window.start_date.strftime("%m/%d/%Y"),
        "endDate": window.end_date.strftime("%m/%d/%Y"),
        "gameType": ",".join(window.game_types),
        "hydrate": "team,venue,linescore",
    }
    if window.team_id:
        params["teamId"] = window.team_id
    return statsapi.get("schedule", params)


def count_games(payload: dict) -> int:
    return sum(len(d.get("games", [])) for d in payload.get("dates", []))


def stage(window: Window, raw_dir: Path = RAW_DIR) -> tuple[Path, int]:
    """Fetch one window and write it to raw_data/games/. Returns (path, games)."""
    payload = fetch(window)
    raw_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = raw_dir / f"schedule_{window.slug()}_{stamp}.json"

    envelope = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "window": window.to_dict(),
        "payload": payload,
    }
    path.write_text(json.dumps(envelope, indent=2))
    return path, count_games(payload)


def stage_all(windows: list[Window], raw_dir: Path = RAW_DIR) -> list[tuple[Path, int]]:
    return [stage(w, raw_dir) for w in windows]
