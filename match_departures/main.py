import logging
import os
from pathlib import Path
import sys
import time
from uuid import uuid4

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    stream=sys.stdout)
logger = logging.getLogger()


engine = create_engine('postgresql://root:rootpassword1234@167.99.243.10/sbahn',
                       executemany_mode='batch'
                      )

path = Path(os.path.dirname(__file__))
line_data = pd.read_csv(path/ '..'/'matching_logic_example'/'line_data.csv')

departures_query = """
set timezone='Europe/Berlin'; 
select d.departure_id, d.destination, SUBSTRING(d.product, 7,2) as line, s.station_name, d.departure_time 
from departures as d, stations as s 
where d.station = s.station_id 
and d.trip_searched=false 
and s.station_name = '{starting_station}' 
and DATE_PART('hour', now()::timestamp - d.departure_time) > 2 
;
"""

next_stop_query = """
select d.departure_id, d.destination, SUBSTRING(d.product, 7,2) as line, s.station_name, d.departure_time \
from departures as d, stations as s \
where d.station = s.station_id \
and d.trip_searched=false \
and s.station_name = '{station}' \
and d.destination = '{destination}' \
and SUBSTRING(d.product, 7,2) = '{line}'
and d.departure_time > '{departure_time}' \
and d.departure_time <= '{offset_time}' \
;\
"""

update_query = """
UPDATE departures
SET trip_searched = true,
    trip_id = '{trip_id}'
WHERE departure_id in ('{departure_ids}'); """

def match_complete_trip():
    for current_line_id in line_data.line_id.unique().tolist():
        logger.info(f"Starting line: {current_line_id}")
        # select current line data
        current_line = line_data[line_data.line_id.eq(current_line_id)]
        first_stop = current_line[current_line['order'].eq(1)]['from'].values[0]
        starting_departure = departures_query.format(starting_station = first_stop)
        # getting starting station to be matched
        starting_departures = pd.read_sql(starting_departure, engine)
        for i, current_start in starting_departures.iterrows():
            logger.info(f"Starting a trip")
            trip = []
            current_start = pd.DataFrame(current_start).T
            try:
                for _, row in current_line.sort_values(by='order', ascending=True).iterrows():
                    if len(trip) == 0:
                        trip.append(current_start.copy())
                        continue
                    station = row['from']
                    line = row['line']
                    destination = trip[-1].destination.values[0]
                    departure_time = trip[-1].departure_time.values[0]
                    offset_time = departure_time + pd.Timedelta(row.delta+5, unit='m')
                    # check if we made it to end of destination
                    if station == destination:
                        logger.info('Found trip from start to destination start: {} end: {}'.format(current_start.departure_id.values[0], trip[-1].departure_id.values[0]))
                        break

                    # search for next stop
                    next_stop_q = next_stop_query.format(station=station, line=line, departure_time=departure_time, offset_time=offset_time, destination=destination)
                    next_stop = pd.read_sql(next_stop_q, engine)

                    # if there is a match save it
                    if next_stop.shape[0] > 0:
                        trip.append(next_stop.sort_values(by='departure_time', ascending=True).head(1).copy())
                    #otherwise break process and remove records except for first
                    else:
                        logger.info('No compelete trip found for {} only found {} stops'.format(current_start.departure_id.values[0], len(trip)))
                        trip = [trip[0]]
                        break
            except Exception as e:
                logger.warn('No compelete trip found for {} the following exception occureed: {}'.format(current_start.departure_id.values[0], str(e)))
                trip = [trip[0]]
                break
            # making sure it runs and then breaking out
            # break
            tmp = pd.concat(trip)
            trip_id = uuid4()
            departure_ids = tmp.departure_id.to_list()
            update_q = update_query.format(trip_id=trip_id, departure_ids="','".join(departure_ids))
            engine.execute(update_q)
        # making sure it runs and then breaking out
        # break

if __name__ == "__main__":
    while True:
        match_complete_trip()
        time.sleep(60)

    #match_complete_trip()