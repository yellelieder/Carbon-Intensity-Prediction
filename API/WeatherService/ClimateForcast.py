import logging
import requests
import json
import logging
from datetime import datetime
import math

WEATHER_DATA_API_KEY="89f83e40489b5e87c4cb16463dc68b42"

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

def parser(s):
    '''
    Parses dates from csv into date object.

        Parameters:
        ----------
        s : str
            Timestapm in csv

        Returns:
        ----------
        date : datetime
            Object of form dd/mm/yyyy hh:mm:ss
    '''
    return datetime.strptime(s,"%d/%m/%Y %H:%M:%S")

def get_url(lat, lng):
    '''
    Turns geo-coordinates in weather api url.

        Parameters:
        ----------

        lat : str
            Lattitude of the place where energy is going to be consumed.

        lng : str
            Longitude of the place where energy is going to be consumed.

        Returns:
        ----------

        url : str
            Url with correct parameter for requesting weather data.yoy
    '''

    log.info(f"converting {lat} and {lng} to weather api url")
    return f"https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lng}&units=metric&appid={WEATHER_DATA_API_KEY}"


#https://openweathermap.org/api/one-call-api
def get_forcast(lat, lng, days_from_now, days_total):
    '''
    Turns geo-coordinates in weather forcast.

        Parameters:
        ----------

        lat : str
            Lattitude of the place where energy is going to be consumed.

        lng : str
            Longitude of the place where energy is going to be consumed.

        Returns:
        ----------

        response : str
            Weather forcast for wind and sun, for timeframe requested.
    '''
    #start und ende in unix
    log.info(f"request weather api")
    response=requests.get(get_url(lat,lng)).json()["list"][days_from_now:days_from_now+days_total]
    return response

def get_best_start(lat, lon, start:str, end:str, dur:int):
    dur_in_days = math.ceil(dur/(24*60))
    start_in_days = (parser(start)-datetime.now()).days
    days_total = (parser(end)-parser(start)).days+1
    pred=get_forcast(lat,lon, start_in_days,days_total+1)
    max_wind_speed = 0
    max_wind_day = 0
    min_cloudiness= math.inf
    min_cloud_day = 0
    #a very simple solution in lack of proper domain knowledge
    for day in range(len(pred)-dur_in_days):
        subset_sum_wind=0
        subset_sum_clouds=0
        for day_in_subset in pred[day:day+dur_in_days]:
            subset_sum_wind +=day_in_subset["speed"]
            subset_sum_clouds +=day_in_subset["clouds"]
        if subset_sum_wind>max_wind_speed:
            max_wind_day=day
            max_wind_speed=subset_sum_wind
        if subset_sum_wind<min_cloudiness:
            min_cloud_day=day
            min_cloudiness=subset_sum_clouds
    start_day = min(max_wind_day, min_cloud_day)
    surise=datetime.utcfromtimestamp(pred[start_day]["sunrise"]).strftime('%H:%M')
    return datetime.utcfromtimestamp(pred[start_day]["dt"]).strftime('%d/%m/%Y')+" "+surise +":00"

if __name__=="__main__":
    print(get_best_start("51.4582235","7.0158171","22/09/2021 21:30:00", "23/09/2021 04:20:00", 2160))