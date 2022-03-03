import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
url = "https://airlabs.co/api/v9/flights?_view=array&_fields=hex,flag,lat,lng,dir,alt&api_key=ae5dd420-49c7-4c0a-8512-f317e666207a"

response = requests.get(url,).json
print(response)
import json
with open('airlines.json', 'w') as json_file:
    json.dump(response, json_file)