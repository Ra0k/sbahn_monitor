from psycopg2 import sql
from utils import convert_timestamp
import psycopg2


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


def create_stations_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "public"."stations" (
            "station_id" varchar(32),
            "station_name" varchar(32),
            PRIMARY KEY ("station_id")
        );
        """)


def create_lines_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "public"."lines" (
            "line" varchar(16) NOT NULL,
            "station_id" varchar(32),
            "start" varchar(32),
            "end" varchar(32),
            "order" int4,
            PRIMARY KEY ("line", "station_id", "start", "end")
        );
        """)

def create_claims_table(cur):
    cur.execute("""
        CREATE TABLE "public"."claims" (
            "claim_id" int2 NOT NULL,
            "text" varchar(254),
            PRIMARY KEY ("claim_id")
        );
        """)


def create_reports_table(cur):
    cur.execute("""
        CREATE TABLE "public"."reports" (
            "created_at" timestamp,
            "station_id" varchar(32),
            "claim_id" int2
        );
        """)


def get_station_id(cur, station_name):
    cur.execute(
        sql.SQL("""
        SELECT 
            station_id,
            station_name
        FROM stations WHERE station_name = (%s);
        """), (station_name, ))

    station = cur.fetchone()

    station_id = None
    if station and len(station) == 2:
        (station_id, _) = station

    return station_id


def insert_station(cur, station):
    cur.execute(
        """
            INSERT INTO stations (
                station_id,
                station_name
            ) VALUES (%s, %s)
        """, (
            station['station_id'], station['station_name']
        )
    )


def insert_line_station(cur, line, station):
    cur.execute(
        """
            INSERT INTO lines (
                line,
                station_id,
                start,
                "end",
                "order"
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            line['line'], station['station_id'], line['start'], line['end'], station['order']
        )
    )


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