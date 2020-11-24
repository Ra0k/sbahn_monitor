from pprint import pprint
from utils import raise_message

import requests
import json


URL_BASE = 'https://www.mvg.de/api'


@raise_message('MVV API CALL: Find Station Failed')
def find_stations(name):
    if name is None:
        raise Exception('Station name cannot be empty!')

    num_locations = 0
    for _ in range(2):
        url = f'{URL_BASE}/fahrinfo/location/queryWeb?q={name}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f'Request for finding station failed! status code: {response.status_code}\n text: {response.text}')
        
        response = json.loads(response.text)

        num_locations = len(response.get('locations', []))
        if num_locations > 0:
            break

    return response['locations']


@raise_message('MVV API CALL: Find SBahn Station Failed')
def find_sbahn_station(name):
    response = find_stations(name)

    response = [
        item for item in response if 'SBAHN' in item.get('products', [])
    ]

    return response


@raise_message('MVV API CALL: Find SBahn Station In City Failed')
def find_sbahn_station_in_city(name, city='München'):
    response = find_stations(name)

    response = [
        item for item in response if (item['place'] == city and 'SBAHN' in item['products'])
    ]

    return response


@raise_message('MVV API CALL: Departure Information')
def departure_information(station_id):
    if station_id is None:
        raise Exception('Station id cannot be empty!')

    url = f'{URL_BASE}/fahrinfo/departure/{station_id}?footway=0'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Request for departure information failed! status code: {response.status_code}\n text: {response.text}')

    response = json.loads(response.text)

    num_departures = len(response['departures'])
    for i in range(num_departures):
        if 'delay' not in response['departures'][i]:
            response['departures'][i]['delay'] = 0
        if isinstance(response['departures'][i]['platform'], str):
            platforms = [int(part) for part in response['departures'][i]['platform'].split() if part.isdigit()]
            if len(platforms) > 0:
                response['departures'][i]['platform'] = platforms[0]
            else:
                response['departures'][i]['platform'] = -1

    return response
