from datetime import datetime
from psycopg2 import sql
import psycopg2

convert_timestamp = lambda x : datetime.fromtimestamp(x / 1e3)

def connect(db_url):
    conn = psycopg2.connect(db_url)
    conn.autocommit = False

    return conn


def get_departure(cur, departure_id):
    cur.execute(
        sql.SQL("""
        SELECT 
            created_at, 
            updated_at, 
            departure_id, 
            delay, 
            passed_before, 
            destination, 
            platform, 
            cancelled 
        FROM departures WHERE departure_id = (%s);
        """), (departure_id, ))

    departure = cur.fetchone()

    return departure

