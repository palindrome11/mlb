import os
import tzlocal
from psycopg2.extensions import connection
from basecamp.db import connect 

def set_client_timezone():
    localtz = tzlocal.get_localzone_name()
    print(localtz)
    os.environ["PGTZ"] = localtz  


set_client_timezone()



