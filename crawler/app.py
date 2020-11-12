from utils import get_env, diff_datetime
from datetime import datetime
from stations import STATIONS

import db_manager
import mvv_reader
import time

ROUND_LENGTH = 60
only_sbahn = lambda x: [dep for dep in x if dep['product'] == 'SBAHN']

def process_station(conn, station):
    cur = conn.cursor()

    stations = mvv_reader.find_sbahn_station(station)
    station_id = stations[0]['id']
    info = mvv_reader.departure_information(station_id)

    current_time = datetime.now().isoformat()

    for departure in only_sbahn(info['departures']):
        departure['station'] = station_id
        dep_db = db_manager.get_departure(cur, departure['departureId'])

        if not (dep_db and len(dep_db) == 8 and dep_db[5] == departure['destination']):
            departure['created_at'] = departure['updated_at'] = current_time
            db_manager.insert_departure(cur, departure)
        else:
            (created_at, updated_at, _, delay, _, destination, platform, cancelled) = dep_db
            fields = {}
            if delay != departure['delay']: fields['delay'] =  departure['delay']
            if platform != departure['platform']: fields['platform'] =  departure['platform']
            if cancelled != departure['cancelled']: fields['cancelled'] =  departure['cancelled']

            if fields:
                fields['updated_at'] = current_time
                db_manager.update_departure(cur, departure['departureId'], fields)


    conn.commit()
    print(f'🆗 {station}')


db_url = 'postgresql://david.szabo@127.0.0.1/sbahn'
conn = db_manager.connect(db_url)


while True:
    start = datetime.now()
    for station in STATIONS:
        try:
            process_station(conn, station)
        except Exception as e:
            print(f'🚫 {station}')

    length = diff_datetime(start, datetime.now())
    print(f'☆☆☆☆☆☆☆☆☆ Round S8 ended in {length} seconds ☆☆☆☆☆☆☆☆☆')
    if length < 60:
        time.sleep(ROUND_LENGTH-length)