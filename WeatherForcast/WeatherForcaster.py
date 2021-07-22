import requests
import json


WEATHER_DATA_API_KEY="89f83e40489b5e87c4cb16463dc68b42"

def getUrl(lat, lng):
    '''Converts geo coordinated into weather API url'''
    return f"https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lng}&units=metric&appid={WEATHER_DATA_API_KEY}"


#https://openweathermap.org/api/one-call-api
def getForcast(lat, lng):
    """Converts geo coordinates in wind and sun prediction."""
    #start und ende in unix
    response=requests.get(getUrl(lat,lng)).json()
    return response

if __name__=="__main__":
    #nur wenn Anfrage in den nächsten 30 Tage
    #dann genau für den Zeitraum
    print(json.dumps(getForcast("51.4582235","7.0158171"), indent=1))

#sonnenstunden
#uv index
#windstärke