import math
from datetime import datetime
from types import FrameType
from app.prediction import predictor
import os
import importlib
from app.forcast import climate
from app.forcast import weather
import csv
from app.prediction import evaluator
from app.helpers import common
import logger as log

def run(lat, lng, start, end, dur, test):
    days_in_future=(common.str_to_datetime(start)-datetime.now()).days
    if test=="test":
        prediction = predictor.ar_prediction(start, end, dur)
        target = evaluator.run(start, end, dur)[0]
        randome = evaluator.run(start, end, dur)[1]
        result=(prediction==target)
        randome=(randome==target)
        return prediction, result, randome
    if(days_in_future<30):
        if(days_in_future<4):
            return weather.ar_prediction(lat, lng, start, end, dur)
        else:
            if(math.ceil(dur/60))<24:
                return predictor.ar_prediction(start, end, dur)
            else:
                return climate.ar_prediction(lat, lng, start, end, dur)
    else:
        return predictor.ar_prediction(start, end, dur)
