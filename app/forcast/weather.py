import logging
from types import resolve_bases
import requests
import json
import logging
from datetime import datetime
import math
import config
from app.helpers import common
import logger as log

def _get_url(lat, lng):
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
                Url with correct parameter for requesting weather data.
    '''
    result=f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lng}&units=metric&appid={config.openweathermap_org_api_key}"
    log.add.info(f"converting {lat} and {lng} to weather api url")
    return result

def _get_forcast(lat, lng)->json:
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

            response : json
                Weather forcast for wind and sun, for timeframe requested.
    '''
    try:
        response=requests.get(_get_url(lat,lng)).json()
    except requests.exceptions.RequestException:
        print("openweathermap.org weather forcast was not succefull, first check api keys")
        log.add.info(f"weather forcast failed")
    log.add.info(f"requested weather api lat {lat}, lng {lng}")
    return response

def get_best_start(lat, lon, start:str, end:str, dur:int):
    '''
    Turns request parameters into weather forcast-based prediction.

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
    start = common.str_to_datetime(start)
    end = common.str_to_datetime(end)
    dur_in_hours = math.ceil(dur/60)
    start_in_hours = math.ceil((start-datetime.now()).seconds/3600)
    hours_total = math.ceil((end-start).seconds/3600) 
    pred=_get_forcast(lat,lon)
    sunrise=pred["city"]["sunrise"]
    pred= pred["list"][start_in_hours:start_in_hours+hours_total]
    max_wind_speed, max_wind_day, min_cloud_day, min_cloudiness = 0,0,0,math.inf
    for hour in range(len(pred)-dur_in_hours):
        subset_sum_wind, subset_sum_clouds=0,0
        for hour_in_subset in pred[hour:hour+dur_in_hours]:
            subset_sum_wind +=hour_in_subset["wind"]["speed"]
            subset_sum_clouds +=hour_in_subset["clouds"]["all"]
        if subset_sum_wind>max_wind_speed:
            max_wind_day=hour
            max_wind_speed=subset_sum_wind
        if subset_sum_wind<min_cloudiness:
            min_cloud_day=hour #for fast logic adaptation, just use clouds instead of wind
            min_cloudiness=subset_sum_clouds
    start_hour = max_wind_day
    surise=datetime.utcfromtimestamp(sunrise).strftime('%H:%M')
    sug=common.str_to_datetime(datetime.utcfromtimestamp(pred[start_hour]["dt"]).strftime('%d/%m/%Y')+" "+surise +":00")
    ideal_time=sug if sug>start else start
    result=common.format_date(ideal_time)
    log.add.info(f"weather forcast successfull, result: {result}")
    return result