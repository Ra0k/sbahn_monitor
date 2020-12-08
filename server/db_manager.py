from datetime import datetime
from psycopg2 import sql
from utils import convert_timestamp
import psycopg2


def connect(db_url):
    conn = psycopg2.connect(db_url)
    conn.autocommit = False

    return conn


def get_stations(cur):
    cur.execute(
        sql.SQL("""
        SELECT 
            station_id,
            station_name
        FROM stations;
        """))

    records = cur.fetchall()

    stations = []
    for record in records:
        station_id, station_name = record
        stations.append({
            'station_id': station_id,
            'station_name': station_name
        })

    return stations


def get_line_stations(cur, line):
    cur.execute(
        sql.SQL("""
        SELECT 
            l.order,
            l.line,
            l.station_id,
            s.station_name
        from 
            lines l
        LEFT JOIN stations s
            ON (s.station_id = l.station_id)
        WHERE
            line like (%s);
        """), (line + '%',))

    records = cur.fetchall()

    lines = {
        'name': line, 
        'tracks': []
    }
    for record in records:
        order, line, station_id, station_name = record
        if line not in lines:
            lines[line] = []
            lines['tracks'].append(line)
        
        lines[line].append({
            'order': order,
            'station_id': station_id,
            'station_name': station_name
        })

    return lines


def get_incoming_departures_by_station_id(cur, station_id):
    cur.execute(
        sql.SQL("""
        SELECT 
            created_at, 
            updated_at, 
            station,
            s.station_name as station_name,
            departure_id, 
            departure_time,
            delay, 
            product,
            destination, 
            platform, 
            cancelled 
        FROM 
            departures 
        LEFT JOIN stations s
            on (s.station_id = station)
        WHERE 
            station = (%s) and 
            departure_time + delay * interval '1 minutes' > now();
        """), (station_id, ))

    records = cur.fetchall()

    departures = []
    for record in records:
        departures.append({
            'created_at': record[0],
            'updated_at': record[1],
            'station': record[2],
            'station_name': record[3],
            'departure_id': record[4],
            'departure_time': record[5],
            'delay': record[6],
            'product': record[7],
            'destination': record[8],
            'platform': record[9],
            'cancelled': record[10]
        })

    return departures
