import socket
import tzlocal
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor, execute_values
from basecamp.db import connect

def client_id() -> str:
    """Stable client name: hostname without the domain suffix, lowercased."""
    return socket.gethostname().split(".")[0].lower()     # 'ana'

def register_client(conn: connection) -> tuple[str, str]:
    """Record this machine's time zone in client_config (insert or update)."""
    client_name: str = socket.gethostname()
    client_name: str = client_id()
    local_tz: str = tzlocal.get_localzone_name()
    UPSERT_SQL = """
    INSERT INTO client_config (client_name, local_tz)
    VALUES (%s, %s)
    ON CONFLICT (client_name)
    DO UPDATE SET local_tz = EXCLUDED.local_tz,
                  updated_at = now();
    """
    with conn:
        with conn.cursor() as cur:
            cur.execute(UPSERT_SQL, (client_name, local_tz))
    return client_name, local_tz

def main():
    conn = connect()
    client_name, local_tz = register_client(conn)
    #print(f"Client Name: {client_name}")
    #print(f"Local Time Zone: {local_tz}")
    print(f"Client Configuration Updated: {client_name} - {local_tz}")


if __name__ == '__main__':
    main()      