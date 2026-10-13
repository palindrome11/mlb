from datetime import datetime, date
import os,sys
import psycopg2
import paths 

def create_client_config():
    CREATE_SQL = """
    CREATE TABLE client_config (
    client_name  text PRIMARY KEY,
    local_tz     text NOT NULL CHECK (now() AT TIME ZONE local_tz IS NOT NULL),
    registered_at timestamptz NOT NULL DEFAULT now(),
    updated_at    timestamptz NOT NULL DEFAULT now()
    );
    """
    
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
    )

    try:
        with conn, conn.cursor() as cur:
            cur.execute(CREATE_SQL)
    finally:
        conn.close()
    print("client_config table ready.")

def main():
    print(f"Python: {sys.executable}")
    print(f"Database: {os.environ.get('DB_NAME')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        create_client_config()
    else:
        print("Run with --create to actually create the table")

if __name__ == '__main__':
    main()      


