bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

CONTAINER=postgres_playground

echo "--- dropping and recreating mlb_dev"
docker exec "$CONTAINER" dropdb -U postgres --force --if-exists mlb_dev
docker exec "$CONTAINER" createdb -U postgres -O mlb_dev_user mlb_dev

