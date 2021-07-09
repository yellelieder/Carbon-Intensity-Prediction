
import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
from regex.regex import DEFAULT_VERSION
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt

PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
CONSUMPTION_MODEL_FOLDER_PATH ="Ressources\\Models Consumption\\"
CONSUMPTION_DATA_FOLDER_PATH="Ressources\\Training Data Consumption\\"
LAST_TRAINING_DATA_POINT="31/12/2020 23:45:00"

def getLatestFile(dir):
        return sorted(os.listdir(dir)).pop()
def timeToIndex(time):
    return int(divmod((datetime.strptime(time, '%d/%m/%Y %H:%M:%S')-datetime.strptime(LAST_TRAINING_DATA_POINT, '%d/%m/%Y %H:%M:%S')).total_seconds(),900)[0])
def indexToTime(index):
    datetime
    return int(divmod((datetime.strptime(time, '%d/%m/%Y %H:%M:%S')-datetime.strptime(LAST_TRAINING_DATA_POINT, '%d/%m/%Y %H:%M:%S')).total_seconds(),900)[0])
def predict(start, end, consumption_or_production):
    #convert datetime into indexed 15 min intervalls
    normalized_start=timeToIndex(start)
    normalized_end=timeToIndex(end)
    if consumption_or_production=="production":
        folder_path=PRODUCTION_MODEL_FOLDER_PATH
    else:
        folder_path=CONSUMPTION_MODEL_FOLDER_PATH
        
    model=sm.load(folder_path+getLatestFile(folder_path))
    return model.predict(start=normalized_start, end=normalized_end, dynamic=False)

def timeSeries(start, end):
    p=predict(start, end, "production")
    c=predict(start, end, "consumption")
    return p.divide(other=c)


#todo: search for best time frame to start
if __name__ == "__main__":
    d=90
    cd=int(d/15)
    time_series=timeSeries("08/07/2021 07:00:00", "08/07/2021 11:00:00",)
    opt_timeframe=0
    recom=0
    for index, value in time_series.items():
        print(time_series)
        print("iloc:")
        print(sum(time_series.iloc[index:index+cd]))
        if sum(time_series.iloc[index:index+cd])>opt_timeframe:
            opt_timeframe=sum(time_series.iloc[index:index+cd])
            recom=index
    print(recom)
