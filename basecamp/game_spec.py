"""Request specs for populating dim_games.

The point of this module: the Streamlit app never talks to the API or the
database directly. It only builds a RequestSpec (plain data, JSON-serializable),
which expand() turns into a list of concrete API request Windows. Anything that
can produce a spec -- the app, a CLI flag, a cron job reading a JSON file --
drives the exact same code path.

Adjust GAME_TYPES / PHASE_BOUNDS if your dim_seasons column names differ.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta

# MLB StatsAPI gameType codes
GAME_TYPES = {
    "S": "Spring training",
    "R": "Regular season",
    "F": "Wild card",
    "D": "Division series",
    "L": "League championship",
    "W": "World series",
    "A": "All-star",
    "E": "Exhibition",
}

# A "phase" is what a person picks; it maps to one or more gameType codes
# and to a pair of boundary columns in dim_seasons.
PHASE_TO_TYPES = {
    "spring": ("S",),
    "regular": ("R",),
    "postseason": ("F", "D", "L", "W"),
    "allstar": ("A",),
}

# The primary key column on dim_seasons.
SEASON_COLUMN = "season"

PHASE_BOUNDS = {
    "spring": ("spring_start_date", "spring_end_date"),
    "regular": ("regular_season_start_date", "regular_season_end_date"),
    "postseason": ("post_season_start_date", "post_season_end_date"),
    "allstar": ("all_star_date", "all_star_date"),
}

PHASE_LABELS = {
    "spring": "Spring training",
    "regular": "Regular season",
    "postseason": "Postseason",
    "allstar": "All-star",
}


class SpecError(ValueError):
    """Raised when a spec can't be turned into API requests."""


@dataclass(frozen=True)
class Window:
    """One concrete API request: a date range plus a set of gameType codes."""

    start_date: date
    end_date: date
    game_types: tuple[str, ...]
    season: int | None = None
    phase: str | None = None
    team_id: int | None = None

    @property
    def days(self) -> int:
        return (self.end_date - self.start_date).days + 1

    @property
    def label(self) -> str:
        phase = PHASE_LABELS.get(self.phase, "Custom range")
        season = self.season or self.start_date.year
        return f"{season} {phase} · {self.start_date} to {self.end_date}"

    def slug(self) -> str:
        """Filename-safe identifier for the staged JSON file."""
        types = "".join(self.game_types)
        return f"{self.season or self.start_date.year}_{types}_{self.start_date}_{self.end_date}"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["start_date"] = self.start_date.isoformat()
        d["end_date"] = self.end_date.isoformat()
        d["game_types"] = list(self.game_types)
        return d


@dataclass
class RequestSpec:
    """What the person asked for, before it's resolved against dim_seasons.

    mode:
      "seasons" -- seasons x phases, boundaries read from dim_seasons
      "range"   -- an explicit start/end date the person picked
      "recent"  -- the last N days ending today (N=1 for a day, 7 for a week)
    """

    mode: str = "seasons"
    seasons: list[int] = field(default_factory=list)
    phases: list[str] = field(default_factory=lambda: ["regular"])
    start_date: date | None = None
    end_date: date | None = None
    lookback_days: int = 7
    team_id: int | None = None
    chunk_days: int = 30  # split long ranges into separate requests/files

    def validate(self) -> None:
        if self.mode not in {"seasons", "range", "recent"}:
            raise SpecError(f"Unknown mode: {self.mode}")
        if not self.phases:
            raise SpecError("Pick at least one game type.")
        bad = set(self.phases) - set(PHASE_TO_TYPES)
        if bad:
            raise SpecError(f"Unknown phase(s): {', '.join(sorted(bad))}")

        if self.mode == "seasons" and not self.seasons:
            raise SpecError("Pick at least one season.")
        if self.mode == "range":
            if not (self.start_date and self.end_date):
                raise SpecError("A custom range needs both a start and an end date.")
            if self.end_date < self.start_date:
                raise SpecError("The end date falls before the start date.")
        if self.mode == "recent" and self.lookback_days < 1:
            raise SpecError("Look back at least one day.")

    def game_types(self) -> tuple[str, ...]:
        codes: list[str] = []
        for phase in self.phases:
            for code in PHASE_TO_TYPES[phase]:
                if code not in codes:
                    codes.append(code)
        return tuple(codes)

    def to_json(self, **kwargs) -> str:
        d = asdict(self)
        for key in ("start_date", "end_date"):
            if d[key] is not None:
                d[key] = d[key].isoformat()
        return json.dumps(d, **kwargs)

    @classmethod
    def from_json(cls, raw: str) -> "RequestSpec":
        d = json.loads(raw)
        for key in ("start_date", "end_date"):
            if d.get(key):
                d[key] = date.fromisoformat(d[key])
        return cls(**d)


def expand(
    spec: RequestSpec,
    season_bounds: dict[int, dict[str, date]] | None = None,
    today: date | None = None,
) -> list[Window]:
    """Resolve a spec into the API requests it implies.

    season_bounds is what you get from dim_seasons:
        {2024: {"regular_season_start_date": date(2024, 3, 20), ...}, ...}
    """
    spec.validate()
    today = today or date.today()
    windows: list[Window] = []

    if spec.mode == "seasons":
        if not season_bounds:
            raise SpecError("Season boundaries weren't loaded from dim_seasons.")
        for season in sorted(spec.seasons):
            bounds = season_bounds.get(season)
            if not bounds:
                raise SpecError(f"dim_seasons has no row for {season}.")
            for phase in spec.phases:
                start_col, end_col = PHASE_BOUNDS[phase]
                start, end = bounds.get(start_col), bounds.get(end_col)
                if not (start and end):
                    # e.g. a season row with no postseason dates yet
                    continue
                windows.append(
                    Window(
                        start_date=start,
                        end_date=end,
                        game_types=PHASE_TO_TYPES[phase],
                        season=season,
                        phase=phase,
                        team_id=spec.team_id,
                    )
                )
    else:
        if spec.mode == "range":
            start, end = spec.start_date, spec.end_date
        else:
            end = today
            start = today - timedelta(days=spec.lookback_days - 1)
        windows.append(
            Window(
                start_date=start,
                end_date=end,
                game_types=spec.game_types(),
                season=start.year if start.year == end.year else None,
                team_id=spec.team_id,
            )
        )

    if not windows:
        raise SpecError("Nothing to request -- those seasons have no dates for the phases you picked.")

    return [chunked for w in windows for chunked in chunk(w, spec.chunk_days)]


def chunk(window: Window, chunk_days: int) -> list[Window]:
    """Split a long window so each API call and each raw file stays small."""
    if chunk_days <= 0 or window.days <= chunk_days:
        return [window]
    out: list[Window] = []
    cursor = window.start_date
    while cursor <= window.end_date:
        stop = min(cursor + timedelta(days=chunk_days - 1), window.end_date)
        out.append(
            Window(
                start_date=cursor,
                end_date=stop,
                game_types=window.game_types,
                season=window.season,
                phase=window.phase,
                team_id=window.team_id,
            )
        )
        cursor = stop + timedelta(days=1)
    return out
