import requests

endpoint = "http://offerup.com/api/graphql"

query = """{
  __schema {
    types {
      name
    }
  }
}
"""

params = {
  'query': query
}

def __post_graphql_request__(query: str):
  s = requests.Session()
  response = s.get(endpoint)
  cookies = dict(response.cookies)
     
  return s.get(endpoint,
               params=params,
               headers={"Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"},
               cookies=cookies,
               timeout=0.2)


gql_response = __post_graphql_request__(query)
print(gql_response.content)