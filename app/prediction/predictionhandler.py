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
    #no logging, to avoide redundancy
    days_in_future=(common.str_to_datetime(start)-datetime.now()).days
    if test=="test":
        prediction = predictor.ar_prediction(start, end, dur)
        target = evaluator.run(start, end, dur)[0]
        randome_direct_hit = evaluator.run(start, end, dur)[1]
        prediction_direct_hit=(prediction==target)
        randome_direct_hit=(randome_direct_hit==target)
        result=prediction, prediction_direct_hit, randome_direct_hit
        log.add.info(f"returned evaluation results")
        return result
    if(days_in_future<30):
        if(days_in_future<4):
            result=weather.get_best_start(lat, lng, start, end, dur)
            log.add.info(f"returned weather forcast-based suggestion ({result})")
            return result
        else:
            if(math.ceil(dur/60))<24:
                result= predictor.ar_prediction(start, end, dur)
                log.add.info(f"returned machine learning-based suggestion ({result})")
                return result
            else:
                result = climate.get_best_start(lat, lng, start, end, dur)
                log.add.info(f"returned climate forcast-based suggestion ({result})")
                return result
    else:
        result= predictor.ar_prediction(start, end, dur)
        log.add.info(f"returned machine learning-based suggestion ({result})")
        return result