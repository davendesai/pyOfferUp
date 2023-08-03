import requests
import json
from pathlib import Path

from lib.openstreetmap import get_exact_coords

from logging import getLogger
logger = getLogger(__name__)

ENDPOINT = "http://offerup.com/api/graphql"

s = requests.Session()
cookies = dict(s.get(ENDPOINT).cookies)

def __get_graphql_request__(q: str, p):
    resp =  s.get(ENDPOINT,
                  params={
                    'query': q,
                    'variables': json.dumps(p)
                  },
                  headers={"Content-Type": "application/json",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"},
                  cookies=cookies,
                  timeout=3.0)

    if resp.status_code != 200:
        logger.error(f"Received {resp.status_code} from https://offerup.com.")
        raise SystemExit

    return json.loads(resp.content)

def get_feed(loc_q: str):
    lat, lon = get_exact_coords(loc_q)

    query = Path('./queries/Feed.gql').read_text()
    params = {
        'searchParams': [
            { 'key': 'platform', 'value': 'web' },
            { 'key': 'limit', 'value': str(50) },
            { 'key': 'lat', 'value': str(lat) },
            { 'key': 'lon', 'value': str(lon) }
        ]
    }
    gql_response = __get_graphql_request__(query, params)
    
    try:
        return gql_response['data']['modularFeed']['looseTiles']
    except:
        logger.error(f"Response from https://offerup.com/api/graphql was unrecognizable.")
        raise SystemExit
        
def get_details(id_q: str):
    query = Path('./queries/ListingDetail.gql').read_text()
    params = {
        'listingId': id_q
    }
    gql_response = __get_graphql_request__(query, params)

    try:
        return gql_response['data']['listing']
    except:
        logger.error(f"Response from https://offerup.com/api/graphql was unrecognizable.")
        raise SystemExit