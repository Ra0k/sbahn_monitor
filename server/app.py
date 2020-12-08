from fastapi import FastAPI
from utils import get_env

import db_manager

app = FastAPI()

db_url = get_env('sbhan_db_conn_url')
conn = db_manager.connect(db_url)

@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.get('/stations')
async def get_stations():
    cur = conn.cursor()
    return db_manager.get_stations(cur)


@app.get('/line/{line}/stations')
async def get_line_stations(line):
    cur = conn.cursor()
    return db_manager.get_line_stations(cur, line)


@app.get('/departures/station/{station_id}')
async def get_departures(station_id):
    cur = conn.cursor()
    return db_manager.get_incoming_departures_by_station_id(cur, station_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
