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


def get_delay_stat(cur, over_type, time_interval, grouped_time):
    if over_type == 'stations':
        target = 'station_name'
        group_by = 'station_name'

    if over_type == 'all':
        target = "null"
        group_by = ''

    time_restriction = ''
    if time_interval == 'current_week':
        time_restriction = 'created_at > now() - interval \'7 days\''
    if time_interval == 'previous_week':
        time_restriction = 'created_at > now() - interval \'14 days\' and created_at < now() - interval \'7 days\''
    if time_interval == 'current_month':
        time_restriction = 'created_at > now() - interval \'1 months\''
    if time_interval == 'previous_month':
        time_restriction = 'created_at > now() - interval \'2 months\' and created_at < now() - interval \'1 months\' '

    group_by_time = ''
    if grouped_time == 'hourly':
        group_by_time = f"date_part('hour', created_at)::int"
    if grouped_time == 'weekday':
        group_by_time = f"date_part('dow', created_at)::int"
    if grouped_time == 'daily':
        group_by_time = f"date_trunc('day', created_at)::date"
    if grouped_time == 'weekly':
        group_by_time = f"date_trunc('week', created_at)::date"
    if grouped_time == 'monthly':
        group_by_time = f"date_trunc('month', created_at)::date"

    add_coma = lambda x: x + ',' if x != '' else x
    add_asc = lambda x: x + ' asc,' if x != '' else x
    if_not_null = lambda x, y: x if any([i != '' for i in x]) else ''

    def gen_group_by(*variables):
        text = ''
        for var in variables:
            if var != '':
                text += f'{var}, '
        if text != '':
            return f'GROUP BY {text}'[:-2]
        return ''
    
    def gen_order_by(*variables):
        text = ''
        for var in variables:
            if var != '':
                text += f'{var}, '
        if text != '':
            return f'ORDER BY {text}'[:-2]
        return ''

    def gen_where(*variables):
        text = ''
        for var in variables:
            if var != '':
                text += f'{var} and '
        if text != '':
            return f'WHERE {text}'[:-4]
        return ''

    cur.execute(
        sql.SQL(f"""
        SELECT
            {add_coma(group_by_time)}
            {target} as target,
            avg(delay) as avg_delay,
            max(delay) as max_delay,
            count(*) as num_all,
            coalesce(sum(case when delay > 0 then 1 end),0) as num_delayed,
            coalesce(round((sum(case when delay > 0 then 1 end)::float / count(*))::numeric, 2),0) delayed
        FROM
            departures d
        LEFT JOIN stations s ON (d.station = s.station_id)
        {gen_where(time_restriction)}
        {gen_group_by(group_by_time, group_by)}
        {gen_order_by(group_by_time, group_by)}
        ;"""))

    records = cur.fetchall()

    if grouped_time in ['hourly', 'daily', 'weekly', 'monthly']:
        delays = {}
        for record in records:
            grouped_time, target_value, avg_delay, max_delay, nAll, nDelayed, ratio = record
            
            if grouped_time not in delays:
                delays[grouped_time] = []

            delay = {
                'avg_delay': avg_delay,
                'max_delay': max_delay,
                '#all': nAll,
                '#delayed': nDelayed,
                '%delayed': ratio
            }

            if target != 'null':
                delay[target] = target_value

            if over_type == 'all':
                delays[grouped_time] = delay
            else:
                delays[grouped_time].append(delay)


    else:
        delays = []
        for record in records:
            target_value, avg_delay, max_delay, nAll, nDelayed, ratio = record
            
            delay = {
                'avg_delay': avg_delay,
                'max_delay': max_delay,
                '#all': nAll,
                '#delayed': nDelayed,
                '%delayed': ratio
            }

            if target != 'null':
                delay[target] = target_value

            delays[grouped_time].append(delay)

    return delays