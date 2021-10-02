import math
from datetime import datetime
from types import FrameType
import Prediction
import os
import importlib
import WeatherService.ClimateForcast
import WeatherService.WeatherForcast


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

def run(lat, lng, start, end, dur):
    days_in_future=(parser(start)-datetime.now()).days
    if(days_in_future<30):
        if(days_in_future<4):
            return WeatherService.WeatherForcast.get_best_start(lat, lng, start, end, dur)
        else:
            if(math.ceil(dur/60))<24:
                return Prediction.get_best_start(start, end, dur)
            else:
                return WeatherService.ClimateForcast.get_best_start(lat, lng, start, end, dur)
    else:
        return Prediction.get_best_start(start, end, dur)
