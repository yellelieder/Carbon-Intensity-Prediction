import logging
import requests
import json
import logging
from datetime import datetime
import math

from requests.models import Request, requote_uri, to_native_string
from app.helpers import common
import config
import logger as log

def _get_url(lat, lng):
    '''
    Turns geo-coordinates in climate api url.

        Parameters:
        ----------

            lat : str
                Lattitude of the place where energy is going to be consumed.

            lng : str
                Longitude of the place where energy is going to be consumed.

        Returns:
        ----------

            url : str
                Url with correct parameter for requesting climate data.
    '''
    url = f"https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lng}&units=metric&appid={config.openweathermap_org_api_key}"
    log.add.info(f"converted {lat} and {lng} to climate api url: {url}")
    return url

def _get_forcast(lat, lng, days_from_now, days_total)->json:
    '''
    Turns geo-coordinates in climate forcast.

        Parameters:
        ----------

            lat : str
                Lattitude of the place where energy is going to be consumed.

            lng : str
                Longitude of the place where energy is going to be consumed.

        Returns:
        ----------

            response : json
                Climate forcast for wind and sun, for timeframe requested.
    '''
    try:
        response=requests.get(_get_url(lat,lng)).json()["list"][days_from_now:days_from_now+days_total]
    except requests.exceptions.RequestException:
        print("openweathermap.org climate forcast was not succefull, first check api keys")
        log.add.info(f"climate forcast failed")
    log.add.info(f"requested climate api lat {lat}, lng {lng}, start in {days_from_now} days, {days_total} total days, result: {response}")
    return response

def get_best_start(lat, lon, start:str, end:str, dur:int):
    '''
    Turns request parameters into climate forcast-based prediction.

        Parameters:
        ----------

            lat : str
                Lattitude of the place where energy is going to be consumed.

            lng : str
                Longitude of the place where energy is going to be consumed.

            start : str
                Start date and time when process can be started.

            end : str
                End date and time when process must be finished.

            dur : string
                Duration how long the computation approximately takes.

        Returns:
        ----------

            response : str
                Suggestion when process should be started.
    '''
    dur_days = math.ceil(dur/(24*60))
    start_days = (common.str_to_datetime(start)-datetime.now()).days
    total_days = (common.str_to_datetime(end)-common.str_to_datetime(start)).days+1
    forcast=_get_forcast(lat,lon, start_days,total_days+1)
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
            min_cloud_day=day #for fast logic adaptation, just use clouds instead of wind
            min_cloud=subset_sum_clouds
    start_day = max_wind_day
    surise=datetime.utcfromtimestamp(forcast[start_day]["sunrise"]).strftime('%H:%M')
    suggestion=common.str_to_datetime(datetime.utcfromtimestamp(forcast[start_day]["dt"]).strftime('%d/%m/%Y')+" "+surise +":00")
    suggestion=suggestion if suggestion>common.str_to_datetime(start) else start
    result= common.format_date(suggestion)
    log.add.info(f"climate forcast successfull, result: {result}")
    return result