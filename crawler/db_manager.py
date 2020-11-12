from datetime import datetime
from psycopg2 import sql
import psycopg2

convert_timestamp = lambda x : datetime.fromtimestamp(x / 1e3)

def connect(db_url):
    conn = psycopg2.connect(db_url)
    conn.autocommit = False

    return conn


def create_departure_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "public"."departures" (
            "created_at" timestamp,
            "updated_at" timestamp,
            "station" varchar(32),
            "departure_id" varchar(64) NOT NULL,
            "departure_time" timestamp,
            "passed_before" timestamp,
            "product" varchar(8),
            "destination" varchar(32),
            "delay" int2,
            "platform" int2,
            "cancelled" bool,
            PRIMARY KEY ("departure_id")
        );
        """)


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


def insert_departure(cur, departure):
    cur.execute(
        """
            INSERT INTO departures (
            created_at,
            updated_at,
            station,
            departure_id,
            departure_time,
            passed_before,
            product,
            destination,
            delay,
            platform,
            cancelled
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            departure['created_at'], departure['updated_at'], departure['station'],
            departure['departureId'], convert_timestamp(departure['departureTime']), departure.get('passedBefore'),
            departure['product'] + ':' + departure['label'], departure['destination'], departure['delay'],
            departure['platform'], departure['cancelled']
        )
    )


def update_departure(cur, departure_id, fields):
    set_part = ','.join(name + ' = %s ' for name, _ in fields.items())[:-1]
    cur.execute(
        """
            UPDATE departures
            SET """ + set_part + """
            WHERE departure_id = %s
        """, (
            *[value for _, value in fields.items()], departure_id
        )
    )