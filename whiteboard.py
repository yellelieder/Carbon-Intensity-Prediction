import requests
import config

response=requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng=50.9917119,10.2136589&result_type=country&key={config.googlemaps_api_key}").json()
print(response)
#["results"][0]["formatted_address"]
