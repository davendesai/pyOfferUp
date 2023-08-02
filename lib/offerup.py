import requests
import json
from pathlib import Path

from lib.openstreetmap import get_exact_coords

from logging import getLogger
logger = getLogger(__name__)

ENDPOINT = "http://offerup.com/api/graphql"
DEFAULT_SEARCH_PARAMS = [
    { 'key': 'platform', 'value': 'web' },
    { 'key': 'limit', 'value': str(50) },
]

class OUResponseException(Exception):
    def __init__(self, code):
        logger.error(f"Received {code} from https://offerup.com.")

class OUGraphQLException(Exception):
    def __init__(self):
        logger.error(f"Response from https://offerup.com/api/graphql was unrecognizable.")

def __get_graphql_request__(q: str, p):
    s = requests.Session()
    response = s.get(ENDPOINT)
    cookies = dict(response.cookies)

    resp =  s.get(ENDPOINT,
                  params={
                    'query': q,
                    'variables': json.dumps({
                      'searchParams': p
                    })
                  },
                  headers={"Content-Type": "application/json",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"},
                  cookies=cookies,
                  timeout=3.0)

    if resp.status_code != 200:
        raise OUResponseException(q, resp.status_code)

    return json.loads(resp.content)

def get_feed(loc_q: str):
    lat, lon = get_exact_coords(loc_q)

    params = DEFAULT_SEARCH_PARAMS + [{
        'key': 'lat', 'value': str(lat),
        'key': 'lon', 'value': str(lon)
    }]

    query = Path('./queries/GetModularFeed.gql').read_text()
    gql_response = __get_graphql_request__(query, params)
    
    try:
        blocks = gql_response['data']['modularFeed']['looseTiles']
        valid_blocks = [b for b in blocks if b.get('tileType', 'INVALID') == 'LISTING']
        return [b.get('listing') for b in valid_blocks]
    except:
        raise OUGraphQLException from None