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
        prediction = predictor.get_best_start(start, end, dur)
        target = evaluator.run(start, end, dur)[0]
        randome = evaluator.run(start, end, dur)[1]
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
            return weather.get_best_start(lat, lng, start, end, dur)
        else:
            if(math.ceil(dur/60))<24:
                return predictor.get_best_start(start, end, dur)
            else:
                return climate.get_best_start(lat, lng, start, end, dur)
    else:
        return predictor.get_best_start(start, end, dur)
