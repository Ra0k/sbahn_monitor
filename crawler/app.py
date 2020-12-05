from multiprocessing import Process
from utils import get_env, diff_datetime, raise_message, convert_timestamp
from datetime import datetime, timedelta
from stations import STATIONS
from error_reporter import get_logger, report

import db_manager
import mvv_reader
import time

ROUND_LENGTH = 60
only_sbahn = lambda x: [dep for dep in x if dep['product'] == 'SBAHN']


@raise_message('Processing Station Failed')
def process_station(conn, station):
    cur = conn.cursor()

    station_id = db_manager.get_station_id(cur, station)
    info = mvv_reader.departure_information(station_id)

    current_time = datetime.now()

    for departure in only_sbahn(info['departures']):
        departure['station'] = station_id
        dep_db = db_manager.get_departure(cur, departure['departureId'])

        if not (dep_db and len(dep_db) == 8 and dep_db[5] == departure['destination']):
            departure['created_at'] = departure['updated_at'] = current_time.isoformat()
            db_manager.insert_departure(cur, departure)
        else:
            (created_at, updated_at, _, delay, _, destination, platform, cancelled) = dep_db
            fields = {}
            if delay != departure['delay']: fields['delay'] =  departure['delay']
            if platform != departure['platform']: fields['platform'] =  departure['platform']
            if cancelled != departure['cancelled']: fields['cancelled'] =  departure['cancelled']
            
            delayed_arrival = convert_timestamp(departure['departureTime']) + timedelta(minutes=departure['delay'])
            if current_time > delayed_arrival: fields['delay'] = abs(current_time - delayed_arrival).minutes

            if fields:
                fields['updated_at'] = current_time.isoformat()
                db_manager.update_departure(cur, departure['departureId'], fields)

    try:
        conn.commit()
        print(f'🆗 {station}')
    except Exception as e:
        conn.rollback()
        print(f'🚫 {station}')


@raise_message('A process failed')
def process_entry(processes=4, key=1):
    db_url = get_env('sbhan_db_conn_url')
    conn = db_manager.connect(db_url)


    while True:
        start = datetime.now()
        for station in [station for idx, station in enumerate(STATIONS) if (idx % processes == key)]:
            try:
                process_station(conn, station)
            except Exception as e:
                conn = db_manager.connect(db_url)
                print(f'❗{station} + {e}')

        length = diff_datetime(start, datetime.now())
        print(f'☆☆☆☆☆☆☆☆☆ Round ended in {length} seconds ☆☆☆☆☆☆☆☆☆')
        if length < ROUND_LENGTH:
            time.sleep(ROUND_LENGTH-length)


@report(get_logger(app_name='Error Reporter'))
def main():
    NUM_OF_PROCESSES = 5

    processes = [
        Process(target=process_entry, args=(NUM_OF_PROCESSES, i)) for i in range(NUM_OF_PROCESSES)
    ]

    for process in processes:
        process.start()

main()