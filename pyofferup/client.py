import requests
import json
from pathlib import Path

endpoint = "http://offerup.com/api/graphql"

# Seattle, WA
search_params = [
  { 'key': 'platform', 'value': 'web' },
  { 'key': 'lon', 'value': '-122.2475' },
  { 'key': 'lat', 'value': '47.7541' },
  { 'key': 'limit', 'value': str(1) },
]

# Boston, MA
search_params2 = [
  { 'key': 'platform', 'value': 'web' },
  { 'key': 'lon', 'value': '-71.0582912' },
  { 'key': 'lat', 'value': '42.3602534', },
  { 'key': 'limit', 'value': str(50) },
]

def __get_graphql_request__(query: str):
  s = requests.Session()
  response = s.get(endpoint)
  cookies = dict(response.cookies)
  
  return s.get(endpoint,
               params={
                 'query': query,
                 'variables': json.dumps({
                   'searchParams': search_params2
                 })
               },
               headers={"Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"},
               cookies=cookies,
               timeout=0.5)

query = Path('./pyofferup/queries/GetModularFeed.gql').read_text()
gql_response = __get_graphql_request__(query)
print(gql_response.status_code)
print(gql_response.content)