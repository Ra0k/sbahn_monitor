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
        """), (station_id,))

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


def get_delay_stat(cur, over_type, time_interval, grouped_time, station_id=None):
    if over_type == 'stations':
        target = 'station_name'
        group_by = 'station_name'

    if over_type == 'all':
        target = "null"
        group_by = ''

    station_restriction = ''
    if station_id is not None:
        station_restriction = f"s.station_id = '{station_id}'"

    time_restriction = ''
    if time_interval == 'current_week':
        time_restriction = 'departure_time > now() - interval \'7 days\''
    if time_interval == 'previous_week':
        time_restriction = 'departure_time > now() - interval \'14 days\' and departure_time < now() - interval \'7 days\''
    if time_interval == 'current_month':
        time_restriction = 'departure_time > now() - interval \'1 months\''
    if time_interval == 'previous_month':
        time_restriction = 'departure_time > now() - interval \'2 months\' and departure_time < now() - interval \'1 months\' '

    group_by_time = ''
    if grouped_time == 'hourly':
        group_by_time = f"date_part('hour', departure_time)::int"
    if grouped_time == 'weekday':
        group_by_time = f"date_part('dow', departure_time)::int"
    if grouped_time == 'daily':
        group_by_time = f"date_trunc('day', departure_time)::date"
    if grouped_time == 'weekly':
        group_by_time = f"date_trunc('week', departure_time)::date"
    if grouped_time == 'monthly':
        group_by_time = f"date_trunc('month', departure_time)::date"

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
        {gen_where(time_restriction, station_restriction)}
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

            delays.append(delay)

    return delays


def get_historical_delay_stats(cur, line, from_station, to_station):
    query = f"""
    select avg(arr.departure_time - dep.departure_time), 
        avg(arr.delay * interval '1' MINUTE),
        sum((arr.delay > 0)::int),
        count(*)
    from (
        select d.departure_time, s.station_name, d.trip_id, d.delay
        from departures as d, stations as s
        where d.station = s.station_id
        and SUBSTRING(d.product, 7,2) = '{line}'
        and d.trip_matched = true
        and s.station_id ='{from_station}'
        ) as dep,
        (
        select d.departure_time, s.station_name, d.trip_id, d.delay
        from departures as d, stations as s
        where d.station = s.station_id
        and SUBSTRING(d.product, 7,2) = '{line}'
        and d.trip_matched = true
        and s.station_id ='{to_station}'
        ) as arr
    where dep.trip_id = arr.trip_id
    and dep.departure_time < arr.departure_time;"""

    cur.execute(sql.SQL(query))
    results = cur.fetchall()
    if len(results) == 0:
        return None
    else:
        avg_duration, avg_delay, n_delayed, n = results[0]
    return {'avg_duration': avg_duration, 'avg_delay': avg_delay, 'percen_delayed': n_delayed / n * 100}


def get_claims(cur):
    cur.execute(
        sql.SQL("""
        SELECT 
            claim_id,
            text
        FROM claims;
        """))

    records = cur.fetchall()

    claims = []
    for record in records:
        claim_id, text = record
        claims.append({
            'claim_id': claim_id,
            'text': text
        })

    return claims


def get_reports(cur):
    cur.execute(
        sql.SQL("""
        select 
            (s.period + interval '1 hour')::timestamp as period,
            count(rep.claim_id) as reports
        from
            generate_series(
                date_trunc('hour', now() - interval '24 hour'),
                date_trunc('hour', now()),
                '1 hour'
            ) as s(period)
            left join reports rep
                on (rep.created_at > period and rep.created_at < period + interval '1 hour')
        group by s.period
        order by s.period desc
        ;
        """))

    overall_records = cur.fetchall()

    cur.execute(
        sql.SQL("""
        select 
            (s.period + interval '1 hour')::timestamp as period,
            rep.station_id,
            stat.station_name,
            count(rep.claim_id) as reports
        from
            generate_series(
                date_trunc('hour', now() - interval '24 hour'),
                date_trunc('hour', now()),
                '1 hour'
            ) as s(period)
            left join reports rep
                on (rep.created_at > period and rep.created_at < period + interval '1 hour')
            left join stations stat
                on (rep.station_id = stat.station_id)
        group by s.period, rep.station_id, stat.station_name
        order by s.period desc, count(*) - 1 desc
        ;
        """))

    detailed_records = cur.fetchall()

    reports = {}
    for record in overall_records:
        period, report_num = record

        reports[period] = {
            'period': period,
            '#reports': report_num, 
            'stations': []
        }

    for record in detailed_records:
        period, station_id, station_name, report_num = record

        if station_id is None: continue 
        reports[period]['stations'].append({
            'station_id': station_id, 
            'station_name': station_name, 
            'report_num': report_num
        })

    return reports


def get_station_report(cur, station_id):
    cur.execute(
        sql.SQL("""
        with base as (
            select 
                * 
            from
                claims as clm,
                generate_series(
                    date_trunc('hour', now() - interval '24 hour'),
                    date_trunc('hour', now()),
                    '1 hour'
                ) as s(period)
        )
        select 
            (b.period + interval '1 hour')::timestamp as period,
            b.claim_id,
            b.text,
            count(rep.claim_id) as reports
        from
            base as b
            left join reports rep
                on ((rep.created_at > period and rep.created_at < period + interval '1 hour') and rep.station_id = %s and b.claim_id = rep.claim_id)
        group by b.period, b.claim_id, b.text
        order by b.period desc, count(*) - 1 desc
        ;
        """), (station_id,))

    records = cur.fetchall()

    report = {}
    for record in records:
        period, claim_id, claim_text, report_num = record

        if period not in report:
            report[period] = []

        report[period].append({
            'claim_id': claim_id,
            'claim_text': claim_text,
            'report_num': report_num
        })

    return report


def add_station_report(cur, station_id, claim_id):
    cur.execute(
        sql.SQL("""
        SELECT 
            claim_id,
            text
        FROM claims
        WHERE 
            claim_id = %s;
        """), (claim_id, ))

    claim = cur.fetchone()
    if not claim or len(claim) != 2:
        return {'response': 'failed', 'response_code': 400}

    cur.execute(
        sql.SQL("""
        SELECT 
            station_id,
            station_name
        FROM stations
        WHERE 
            station_id = %s;
        """), (station_id, ))

    station = cur.fetchone()
    if not station or len(station) != 2:
        return {'response': 'failed', 'response_code': 400}

    cur.execute(
        """
            INSERT INTO reports (
                created_at,
                station_id,
                claim_id
            ) VALUES (%s, %s, %s)
        """, (
            datetime.now().isoformat(), station_id, claim_id
        )
    )

    return {'response': 'successful', 'response_code': 200}