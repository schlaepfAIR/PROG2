import requests
# there is inbuilt json() constructor for requests.get() method
json_data = requests.get("https://airlabs.co/api/v9/schedules?dep_iata=ZRH&airline_iata=LX&api_key=ae5dd420-49c7-4c0a-8512-f317e666207a").json()
print(json_data)

# To actually write the data to the file, we just call the dump() function from json library
import json
with open('personal1.json', 'w') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

with open('personal1.json') as f:
  data = json.load(f)
print(data)

flx = json.dumps(data, ensure_ascii=False, indent=4)
print(flx)
