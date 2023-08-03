import requests
import json

from logging import getLogger
logger = getLogger(__name__)

ENDPOINT = "https://nominatim.openstreetmap.org/search"

def get_exact_coords(q: str) -> (float, float):
    resp = requests.get(ENDPOINT,
                        params={
                            'q': q,
                            'format': 'jsonv2'
                        },
                        timeout=3.0) 
    if resp.status_code != 200:
        logger.error(f"Received {resp.status_code} from https://nominatim.openstreetmap.org.")
        raise SystemExit
    
    try:
        data = json.loads(resp.content)
        lat, lon = data[0]['lat'], data[0]['lon']

        logger.info(f"Query: {q} -> Got Latitude: {lat}, Longitude: {lon}")
        return lat, lon
    except:
        logger.error(f"Location for query: {q} was unable to be determined.")
        raise SystemExit
