from utils import get_env

import db_manager
import mvv_reader
import stations


db_url = get_env('sbhan_db_conn_url') #'postgresql://david.szabo@127.0.0.1/sbahn'
conn = db_manager.connect(db_url)


# CREATE TABLES

cur = conn.cursor()
db_manager.create_departure_table(cur)
db_manager.create_stations_table(cur)
db_manager.create_lines_table(cur)


# INSERT STATIONS

print(stations.STATIONS)

for station in stations.STATIONS:
    station_id = db_manager.get_station_id(cur, station)
    if station_id is None:
        found_stations = mvv_reader.find_sbahn_station(station)
        station_id = found_stations[0]['id']
        obj = {
            'station_name': station, 
            'station_id': station_id
        }
        db_manager.insert_station(cur,obj)


# INSERT LINE INFORMATION

for line, line_stations in stations.LINES.items():
    start = line_stations[0]
    end = line_stations[-1]

    for idx, station in enumerate(line_stations):
        station_id = db_manager.get_station_id(cur, station)
        line_obj = {
            'line': line,
            'start': start,
            'end': end
        }
        station_obj = {
            'station_id': station_id,
            'order': idx+1
        }
        db_manager.insert_line_station(cur, line_obj, station_obj)


conn.commit()