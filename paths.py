from pathlib import Path
from dotenv import load_dotenv

def project_root(marker='.git'):
    for parent in Path(__file__).resolve().parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"No {marker} found above {__file__}")


PROJECT_DIR  = project_root()
RAW_DATA     = PROJECT_DIR / "raw_data" / "daily_rosters"
ARCHIVE_PATH = RAW_DATA / "archive"
SQL_DIR      = PROJECT_DIR / "sql"
LOGS_DIR     = PROJECT_DIR / "logs"
DOCS_DIR     = PROJECT_DIR / "docs"
ENV_FILE     = PROJECT_DIR / ".env"

for _d in (RAW_DATA, ARCHIVE_PATH, LOGS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

_env_loaded = load_dotenv(ENV_FILE)
if not _env_loaded:
    raise RuntimeError(
        f"No .env found at {ENV_FILE}. Copy .env.example and fill it in."
    )