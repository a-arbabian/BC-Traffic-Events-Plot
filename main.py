import gmplot
import requests
from pathlib import Path
import time

starttime = time.time()

script_location = Path(__file__).absolute().parent
file_location = script_location / 'key.txt'
f = file_location.open()
api_key = f.readline()
f.close

colors = {
    "CONSTRUCTION": 'orange',
    "INCIDENT": 'red',
    "SPECIAL_EVENT": 'black',
    "WEATHER_CONDITION": 'blue'
}
activePoints = {
    "CONSTRUCTION": [],
    "INCIDENT": [],
    "SPECIAL_EVENT": [],
    "WEATHER_CONDITION": []
}

gmap = gmplot.GoogleMapPlotter(49.311284, -123.149669, 12, apikey = api_key)

# This particular URL fetches ACTIVE evens in the Lower Main Land
eventsURL = 'http://api.open511.gov.bc.ca/events?format=json&status=ACTIVE&area_id=drivebc.ca%2F1'

while (True):
    response = requests.get(eventsURL)
    data = response.json()
    for s in data["events"]:
        for latlon in s["geography"]["coordinates"]:
            if type(latlon) == list:
                activePoints[s["event_type"]].append((latlon[1],latlon[0]))


    #gmap.heatmap(lats, lons)
    for eventType in activePoints:
        try:
            lats, lons = zip(*activePoints[eventType])
            gmap.scatter(lats, lons, colors[eventType], size=40, marker=False)
        except ValueError:
            print(f"Currently no {eventType.lower()} events.")
    print("Running...")
    time.sleep(5.0 - ((time.time() - starttime) % 5.0)) #Update markers every 5 seconds
    gmap.draw("my_map.html")