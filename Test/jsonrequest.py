import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
url = "https://test.api.amadeus.com/v1/airport/direct-destinations?departureAirportCode=ZRH&max=2"

response = requests.get(url, auth=BearerAuth('5mzGT9C1ZrK9TMfkcQQfoIaILwnB'))
print(response)