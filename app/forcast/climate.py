import logging
import requests
import json
import logging
from datetime import datetime
import math
from app.helpers import common

WEATHER_DATA_API_KEY="89f83e40489b5e87c4cb16463dc68b42"

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

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
    log.info(f"request weather api")
    response=requests.get(get_url(lat,lng)).json()["list"][days_from_now:days_from_now+days_total]
    return response

def get_best_start(lat, lon, start:str, end:str, dur:int):
    dur_days = math.ceil(dur/(24*60))
    start_days = (common.str_to_datetime(start)-datetime.now()).days
    total_days = (common.str_to_datetime(end)-common.str_to_datetime(start)).days+1
    forcast=get_forcast(lat,lon, start_days,total_days+1)
    max_wind_speed,max_wind_day,min_cloud_day = 0,0,0
    min_cloud= math.inf
    for day in range(len(forcast)-dur_days):
        subset_sum_wind, subset_sum_clouds=0,0
        for day_in_subset in forcast[day:day+dur_days]:
            subset_sum_wind +=day_in_subset["speed"]
            subset_sum_clouds +=day_in_subset["clouds"]
        if subset_sum_wind>max_wind_speed:
            max_wind_day=day
            max_wind_speed=subset_sum_wind
        if subset_sum_wind<min_cloud:
            min_cloud_day=day
            min_cloud=subset_sum_clouds
    start_day = min(max_wind_day, min_cloud_day)
    surise=datetime.utcfromtimestamp(forcast[start_day]["sunrise"]).strftime('%H:%M')
    suggestion=common.str_to_datetime(datetime.utcfromtimestamp(forcast[start_day]["dt"]).strftime('%d/%m/%Y')+" "+surise +":00")
    suggestion=suggestion if suggestion>common.str_to_datetime(start) else start
    return common.format_date(suggestion)