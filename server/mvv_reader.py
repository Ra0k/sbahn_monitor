from pprint import pprint
from utils import raise_message
from datetime import datetime, timedelta

import requests
import json


URL_BASE = 'https://www.mvg.de/api'

convert_timestamp = lambda x: datetime.fromtimestamp(x / 1e3)

#@raise_message('MVV API CALL: Find Route Failed')
def find_route(from_station_id, to_station_id):
    if from_station_id is None:
        raise Exception('from_station_id cannot be empty!')
    if to_station_id is None:
        raise Exception('to_station_id cannot be empty!')

    num_locations = 0
    for _ in range(2):
        url = f'{URL_BASE}/fahrinfo/routing/?fromStation={from_station_id}&toStation={to_station_id}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f'Request for finding route has failed! status code: {response.status_code}\n text: {response.text}')
        
        response = json.loads(response.text)

        num_locations = len(response.get('connectionList', []))
        if num_locations > 0:
            break

    connection_list = response.get('connectionList', [])
    if connection_list == []:
        return {}

    response = {
        'from': connection_list[0].get('from'),
        'to': connection_list[0].get('to'),
        'routes': []
    }
    for connection in connection_list:
        route = {
            'departure': convert_timestamp(connection.get('departure')),
            'arrival': convert_timestamp(connection.get('arrival')),
            'ring_from': connection.get('ringFrom'),
            'ring_to': connection.get('ringTo'),
            'connections': []
        }

        first_part = True
        for part_connection in connection.get('connectionPartList', []):
            
            if part_connection.get('delay') is None:
                part_connection['delay'] = 0
            
            if first_part:
                current_time = datetime.now()
                print(current_time)
                delayed_arrival = convert_timestamp(part_connection.get('departure')) + timedelta(minutes=part_connection.get('delay'))
                if current_time > delayed_arrival: part_connection['delay'] = int(abs(current_time - delayed_arrival).seconds / 60)

                first_part = False

            connection = {
                'departure': convert_timestamp(part_connection.get('departure')),
                'departurePlatform': part_connection.get('departurePlatform'),
                'arrival': convert_timestamp(part_connection.get('arrival')),
                'arrivalPlatform': part_connection.get('arrivalPlatform'),
                'delay': part_connection.get('delay'),
                'product': part_connection.get('product'),
                'label': part_connection.get('label'),
                'destination': part_connection.get('destination'),
                'cancelled': part_connection.get('cancelled'),
                'inner_stops': []
            }
            for stop in part_connection.get('stops', []):
                if stop.get('delay') is None:
                    stop['delay'] = 0
                connection['inner_stops'].append({
                    'time': convert_timestamp(stop.get('time')),
                    'delay': stop.get('delay'),
                    'station_city': stop.get('location',{}).get('place'),
                    'station_name': stop.get('location',{}).get('name'),
                    'station_id': stop.get('location',{}).get('id')
                })
            route['connections'].append(connection)
        response['routes'].append(route)



    return response
