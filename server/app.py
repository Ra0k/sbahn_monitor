from fastapi import FastAPI, HTTPException

import db_manager
import mvv_reader
from validators import Station, Line


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8081",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db_url = 'postgresql://root:rootpassword1234@167.99.243.10/sbahn'
conn = db_manager.connect(db_url)

STATION_IDS = [obj['station_id'] for obj in db_manager.get_stations(conn.cursor())]
LINES = ['S6','S20','S7','S1', 'S4', 'S8', 'S2', 'S3']

@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.get('/stations')
async def get_stations():
    cur = conn.cursor()
    return db_manager.get_stations(cur)


@app.get('/route/from/{from_station_id}/to/{to_station_id}')
async def get_routes(from_station_id, to_station_id):
    return mvv_reader.find_route(from_station_id, to_station_id)


@app.get('/line/{line}/stations')
async def get_line_stations(line):
    cur = conn.cursor()
    return db_manager.get_line_stations(cur, line)


@app.get('/departures/station/{station_id}')
async def get_departures(station_id):
    cur = conn.cursor()
    return db_manager.get_incoming_departures_by_station_id(cur, station_id)


@app.get('/stats/delay/all/{time_interval}/grouped/{grouped_time}')
async def get_delay_stat(time_interval, grouped_time):
    cur = conn.cursor()
    if time_interval not in ['current_week', 'previous_week', 'current_month', 'previous_month', 'this_year']:
        return {'error': ''}
    if grouped_time not in ['all', 'hourly', 'daily', 'weekly', 'monthly']:
        return {'error': ''}

    return db_manager.get_delay_stat(cur, 'all', time_interval, grouped_time)


@app.get('/stats/delay/stations/{time_interval}/grouped/{grouped_time}')
async def get_delay_stat(time_interval, grouped_time):
    cur = conn.cursor()
    if time_interval not in ['current_week', 'previous_week', 'current_month', 'previous_month', 'this_year']:
        return {'error': ''}
    if grouped_time not in ['all', 'hourly', 'daily', 'weekly', 'monthly']:
        return {'error': ''}

    return db_manager.get_delay_stat(cur, 'stations', time_interval, grouped_time)


@app.get('/stats/delay/{line}/{from_station}/{to_station}')
async def get_stat_line_delay(line, from_station, to_station):
    """
    Returns:

    - **avg_duration**: in seconds
    - **avg_delay**: in seconds
    - **percent_delayed**: percentage of trips with a nonzero delay
    """
    if from_station not in STATION_IDS or to_station not in STATION_IDS:
        raise HTTPException(status_code=422, detail="Station not found")
    if line not in LINES:
        raise HTTPException(status_code=422, detail="Invalid line")
    cur = conn.cursor()
    return db_manager.get_historical_delay_stats(cur, line, from_station, to_station)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
