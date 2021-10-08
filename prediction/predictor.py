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


PRODUCTION_MODEL_FOLDER_PATH="Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionProduction\\"
PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
CONSUMPTION_MODEL_FOLDER_PATH ="Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionConsumption\\"
CONSUMPTION_DATA_FOLDER_PATH="Ressources\\Training Data Consumption\\"

# log=logging.getLogger(__name__)
# log.setLevel(logging.INFO)
# handler=logging.FileHandler("logs.log")
# handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
# log.addHandler(handler)

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

def get_last_date(type:str):
    path = f"Ressources\TrainingData\{type.capitalize()}.pkl"
    df=pd.read_pickle(path)

    return df.iloc[-1,0]

def time_to_period(time,type):
    input_time_index=datetime.strptime(time, '%d/%m/%Y %H:%M:%S')

    base_time_index = get_last_date(type=type)
    #base_time_index=datetime.strptime("14/09/2021 23:45:00", '%d/%m/%Y %H:%M:%S')
    return int(divmod((input_time_index-base_time_index).total_seconds(),900)[0])

def period_to_time(period, start):
    '''
    Turns row index from training data into human readable time.

        Parameters:
        ----------
        period : int
            n-th row in training set, if one woult continue conting. 

        Returns:
        ----------
        date_time : datetime
            Exact time, accurate to 15 minutes.
    '''
    #returns datetime based on n.th 15 min period since last row in training date
    return (datetime.strptime(start, '%d/%m/%Y %H:%M:%S')+timedelta(seconds=period*900)).strftime('%d/%m/%Y %H:%M:%S')

def get_predictions(start, end, type):
    '''
    Returns prediction of the ideal starting point. 

        Parameters:
        ----------

        start : str
            Starting point for timeframe to be predicted.

        end : str
            Last point in time for which prediction must be made.
        
        type : str
            Type of prediction. Can be "production" or "consumption"

        Returns:
        ----------

        prediction : pd.Series
            Containing predictions of elctricity production or consumption.
    '''
    logging.info(f"applining pre trained ar model to user input-----------------------------------------------------")
    norm_start=time_to_period(start, type)
    norm_end=time_to_period(end,type)
    folder_path = PRODUCTION_MODEL_FOLDER_PATH if (type=="production") else CONSUMPTION_MODEL_FOLDER_PATH
    model=sm.load(folder_path+get_latest_file(folder_path))
    return model.predict(start=norm_start, end=norm_end, dynamic=False)

def get_production_consumption_ratio(start, end):
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
    logging.info(f"calculating production/consumption ratios for user input")
    production_prediction=get_predictions(start, end, "production")
    consumption_prediction=get_predictions(start, end, "consumption")
    return production_prediction.divide(other=consumption_prediction).to_frame()

def find_optimum(time_series, duration, start):
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
    logging.info(f"selecting optimal starting time from timeseries")
    norm_duration=int(duration/15)
    max_cummulative_ratio=0
    optimal_period=0
    for period in range(time_series.size-norm_duration):
        subset_sum=sum(time_series.iloc[period: period+norm_duration].values)
        if subset_sum>max_cummulative_ratio:
            max_cummulative_ratio=subset_sum
            optimal_period=period
    return period_to_time(optimal_period, start)

def ar_prediction(start, end, duration):
    time_series=get_production_consumption_ratio(start, end)
    point_in_time =find_optimum(time_series,duration, start)
    logging.info(f"prediction successful")
    return point_in_time

def get_best_start(start, end, duration):
    return ar_prediction(start, end, duration)