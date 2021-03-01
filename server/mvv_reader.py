from pprint import pprint
from utils import raise_message
from datetime import datetime

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

    connection_list = response['connectionList']
    if connection_list == []:
        return {}

    response = {
        'from': connection_list[0]['from'],
        'to': connection_list[0]['to'],
        'routes': []
    }
    for connection in connection_list:
        route = {
            'departure': convert_timestamp(connection['departure']),
            'arrival': convert_timestamp(connection['arrival']),
            'ring_from': connection['ringFrom'],
            'ring_to': connection['ringTo'],
            'connections': []
        }
        for part_connection in connection['connectionPartList']:
            if part_connection.get('delay') is None:
                part_connection['delay'] = 0
            connection = {
                'departure': convert_timestamp(part_connection['departure']),
                'departurePlatform': part_connection['departurePlatform'],
                'arrival': convert_timestamp(part_connection['arrival']),
                'arrivalPlatform': part_connection['arrivalPlatform'],
                'delay': part_connection['delay'],
                'product': part_connection['product'],
                'label': part_connection['label'],
                'destination': part_connection['destination'],
                'cancelled': part_connection['cancelled'],
                'inner_stops': []
            }
            for stop in part_connection['stops']:
                if stop.get('delay') is None:
                    stop['delay'] = 0
                connection['inner_stops'].append({
                    'time': convert_timestamp(stop['time']),
                    'delay': stop['delay'],
                    'station_city': stop['location']['place'],
                    'station_name': stop['location']['name'],
                    'station_id': stop['location']['id']
                })
            route['connections'].append(connection)
        response['routes'].append(route)



    return response
