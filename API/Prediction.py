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
import sys
import logging

PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
CONSUMPTION_MODEL_FOLDER_PATH ="Ressources\\Models Consumption\\"
CONSUMPTION_DATA_FOLDER_PATH="Ressources\\Training Data Consumption\\"

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("prediction.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

def get_latest_file(dir):
    '''
    Returns last file form folder by alphabetical order.

        Parameters:
        ----------
        dir : str
            Folder to search from.

        Returns:
        ----------
        file_name : str
            Name of the last file from the folder in alphabetical order.
    '''
    return sorted(os.listdir(dir)).pop()

def get_latest_training_date():
    '''
    Returns latest date for which training data is available.

        Returns:
        ----------
        date : str
            Latest available date in training data.
    '''
    log.info(f"gathering latest training data")
    p=str(pd.read_csv("Ressources\TrainingData\Production.csv", index_col=0, parse_dates=[1],sep=",").iloc[-1,0]).replace("-","/")
    c=str(pd.read_csv("Ressources\TrainingData\Consumption.csv", index_col=0, parse_dates=[1],sep=",").iloc[-1,0]).replace("-","/")
    return min(p,c)

def time_to_period(time):
    '''
    Converts time to number of 15 min periods since last training data-date.

    Imagine as continuing the row index from the training date up to the requested date.

        Parameters:
        ----------
        time : str
            Time to be converted.

        Returns:
        ----------
        period_id : int
            The index of the period.
    '''
    input_time_index=datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    base_time_index=datetime.strptime(get_latest_training_date, '%d/%m/%Y %H:%M:%S')
    #returns number of 15 min periods between last row in training date and input time
    return int(divmod((input_time_index-base_time_index).total_seconds(),900)[0])

def period_to_time(period, start):
    '''
    Turns row index from training data to human readable time.

        Parameters:
        ----------
        asdf : str
            asdf

        Returns:
        ----------
        asdf : int
            asdf
    '''
    #returns datetime based on n.th 15 min period since last rom in training date
    return (datetime.strptime(start, '%d/%m/%Y %H:%M:%S')+timedelta(seconds=period*900)).strftime('%d/%m/%Y %H:%M:%S')

def predict(start, end, consumption_or_production):
    '''
    asdf

        Parameters:
        ----------
        asdf : str
            asdf

        Returns:
        ----------
        asdf : int
            asdf
    '''
    log.info(f"applining pre trained ar model to user input")
    norm_start=time_to_period(start)
    norm_end=time_to_period(end)
    folder_path = PRODUCTION_MODEL_FOLDER_PATH if (consumption_or_production=="production") else CONSUMPTION_MODEL_FOLDER_PATH
    model=sm.load(folder_path+get_latest_file(folder_path))
    return model.predict(start=norm_start, end=norm_end, dynamic=False)

def timeSeries(start, end):
    '''
    Returns single time series with productioin/sonsumption ratio.

        Parameters:
        ----------
        start : str
            When the time series must start.
        
        end : str
            When the time series must end.

        Returns:
        ----------
        frame : pd.DataFrame
            Data frame with predicted ratios of energy marked data.
    '''
    log.info(f"calculating production/consumption ratios for user input")
    production_prediction=predict(start, end, "production")
    consumption_prediction=predict(start, end, "consumption")
    return production_prediction.divide(other=consumption_prediction).to_frame()

def forcast(time_series, duration, start):
    '''
    Selects best time to start consuming energy from a time series.

        Parameters:
        ----------
        time_series : pd.DataFrame
            Containing predicted production/consumption ratios.
        
        duration : str
            How long the user predicted his process will take.
        
        start : str
            Earliest time for the process to be started.

        Returns:
        ----------
        time : str
            Time when the process should be started.
    '''
    log.info(f"selecting optimal starting time from timeseries")
    norm_duration=int(duration/15)
    max_cummulative_ratio=0
    optimal_period=0
    for period in range(time_series.size-norm_duration):
        subset_sum=sum(time_series.iloc[period: period+norm_duration].values)
        if subset_sum>max_cummulative_ratio:
            max_cummulative_ratio=subset_sum
            optimal_period=period
    return period_to_time(optimal_period, start)

def timeStamp(start, end, duration):
    '''
    asdf

        Parameters:
        ----------
        asdf : str
            asdf

        Returns:
        ----------
        asdf : int
            asdf
    '''
    time_series=timeSeries(start, end)
    #durarion must be in minutes
    recommendation=forcast(time_series,duration, start)
    return recommendation