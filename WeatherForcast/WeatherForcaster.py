import requests
import json


WEATHER_DATA_API_KEY="3034a3db0da1d5f8462d8ae3d4cb3afa"

def getUrl(lat, lng):
    '''Converts geo coordinated into weather API url'''
    return f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lng}&excludet=alerts&appid={WEATHER_DATA_API_KEY}"


#https://openweathermap.org/api/one-call-api
def getForcast(lat, lng):
    """Converts geo coordinates in wind and sun prediction."""
    response=requests.get(getUrl(lat,lng)).json()
    return response

if __name__=="__main__":
    print(json.dumps(getForcast("51.4582235","7.0158171"), indent=1))