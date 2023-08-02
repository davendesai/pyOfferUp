import requests
import json

from logging import getLogger
logger = getLogger(__name__)

ENDPOINT = "https://nominatim.openstreetmap.org/search"

class OSMResponseException(Exception):
    def __init__(self, code):
        logger.error(f"Received {code} from https://nominatim.openstreetmap.org.")

class OSMQueryException(Exception):
    def __init__(self, q):
        logger.error(f"Location for query: {q} was unable to be determined.")

def get_exact_coords(q: str) -> (float, float):
    resp = requests.get(ENDPOINT,
                        params={
                            'q': q,
                            'format': 'jsonv2'
                        },
                        timeout=3.0) 
    if resp.status_code != 200:
        raise OSMResponseException(resp.status_code)
    
    try:
        data = json.loads(resp.content)
        lat, lon = data[0]['lat'], data[0]['lon']

        logger.info(f"Query: {q} -> Got Latitude: {lat}, Longitude: {lon}")
        return lat, lon
    except:
        raise OSMQueryException(q)
