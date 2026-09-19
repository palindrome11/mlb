"""Single place the project builds a Postgres connection.

Everything -- the Streamlit app, the CLI loaders, cron scripts -- imports
connect() from here so there's one definition of how credentials resolve.
"""

from __future__ import annotations

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)


def conn_kwargs(dbname: str | None = None) -> dict:
    """psycopg2.connect() kwargs from the project's DB_* variables.

    dbname overrides DB_NAME -- that's how the app's dev/prod radio works.
    Returns a dict rather than a DSN string so passwords never need escaping.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": dbname or os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.getenv("DB_PASSWORD", ""),
    }


def connect(conn_info: dict | str | None = None):
    """Open a connection. Caller closes it -- use contextlib.closing().

    Accepts a kwargs dict, a DSN string, or nothing (falls back to DB_*).
    """
    if conn_info is None:
        conn_info = conn_kwargs()
    if isinstance(conn_info, str):
        return psycopg2.connect(conn_info)
    return psycopg2.connect(**conn_info)
