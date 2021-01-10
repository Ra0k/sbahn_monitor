from fastapi import FastAPI

from server import db_manager


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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
