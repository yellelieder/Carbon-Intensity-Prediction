import math
from datetime import datetime
from types import FrameType
from Prediction import MLPredictor
import os
import importlib
import WeatherService.ClimateForcast
import WeatherService.WeatherForcast
import csv
from Prediction import EvaluationHelper


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

def run(lat, lng, start, end, dur, test):
    days_in_future=(parser(start)-datetime.now()).days
    if test=="test":
        prediction = MLPredictor.get_best_start(start, end, dur)
        target = EvaluationHelper.run(start, end, dur)[0]
        randome = EvaluationHelper.run(start, end, dur)[1]
        off_by_m=abs((parser(prediction)-parser(target)).days)
        result=(prediction==target)
        randome=(randome==target)
        #fields=[result,start, end, dur,randome, prediction, target, off_by_m]
        # with open(r'Ressources\Models\randomized_evaluation.csv', 'a',newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(fields)
        return prediction, result, randome
    if(days_in_future<30):
        if(days_in_future<4):
            return WeatherService.WeatherForcast.get_best_start(lat, lng, start, end, dur)
        else:
            if(math.ceil(dur/60))<24:
                return MLPredictor.get_best_start(start, end, dur)
            else:
                return WeatherService.ClimateForcast.get_best_start(lat, lng, start, end, dur)
    else:
        return MLPredictor.get_best_start(start, end, dur)
