import pandas as pd
from datetime import datetime, time, timedelta
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
import numpy as np

PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
CONSUMPTION_MODEL_FOLDER_PATH ="Ressources\\Models Consumption\\"
CONSUMPTION_DATA_FOLDER_PATH="Ressources\\Training Data Consumption\\"
LAST_TRAINING_DATA_POINT="31/12/2020 23:45:00"

def getLatestFile(dir):
    return sorted(os.listdir(dir)).pop()

def timeToPeriod(time):
    input_time_index=datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    base_time_index=datetime.strptime(LAST_TRAINING_DATA_POINT, '%d/%m/%Y %H:%M:%S')
    #returns number of 15 min periods between last row in training date and input time
    return int(divmod((input_time_index-base_time_index).total_seconds(),900)[0])

def periodToTime(period, start, end):
    #returns datetime based on n.th 15 min period since last rom in training date
    print("period: "+str(period))
    return (datetime.strptime(start, '%d/%m/%Y %H:%M:%S')+timedelta(seconds=period*900)).strftime('%d/%m/%Y %H:%M:%S')

def predict(start, end, consumption_or_production):
    norm_start=timeToPeriod(start)
    norm_end=timeToPeriod(end)
    if consumption_or_production=="production":
        folder_path=PRODUCTION_MODEL_FOLDER_PATH
    else:
        folder_path=CONSUMPTION_MODEL_FOLDER_PATH
    model=sm.load(folder_path+getLatestFile(folder_path))
    return model.predict(start=norm_start, end=norm_end, dynamic=False)

def timeSeries(start, end):
    production_prediction=predict(start, end, "production")
    consumption_prediction=predict(start, end, "consumption")
    return production_prediction.divide(other=consumption_prediction).to_frame()

def recommend(time_series, duration, start, end):
    norm_duration=int(duration/15)
    max_cummulative_ratio=0
    optimal_period=0
    for period in range(time_series.size-norm_duration):
        subset_sum=sum(time_series.iloc[period: period+norm_duration].values)
        if subset_sum>max_cummulative_ratio:
            max_cummulative_ratio=subset_sum
            optimal_period=period
    return periodToTime(optimal_period, start, end)

if __name__ == "__main__":
    start="08/07/2021 07:00:00"
    end="08/07/2021 11:00:00"
    time_series=timeSeries(start, end)
    #durarion must be in minutes
    rec=recommend(time_series,90, start, end) #returns index of period in timeframe
    print(rec)
