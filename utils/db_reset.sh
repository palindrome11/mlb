bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

CONTAINER=postgres_playground
SCHEMA=docs/schema_dev.sql

[ -f "$SCHEMA" ] || { echo "Missing $SCHEMA"; exit 1; }

echo "--- dropping and recreating mlb_dev"
docker exec "$CONTAINER" dropdb -U postgres --force --if-exists mlb_dev
docker exec "$CONTAINER" createdb -U postgres -O mlb_dev_user mlb_dev

echo "--- applying $SCHEMA"
docker exec -i "$CONTAINER" psql -U mlb_dev_user -d mlb_dev -v ON_ERROR_STOP=1 -q < "$SCHEMA"

echo "--- tables now present"
docker exec "$CONTAINER" psql -U mlb_dev_user -d mlb_dev -c '\dt'
echo "mlb_dev rebuilt — run the loader to repopulate"
