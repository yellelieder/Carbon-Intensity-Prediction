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
from app.helpers import common
import config
import logger as log

def _get_prediction(start, end, type):
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
    norm_start=common.datetime_str_to_lag(start, type)
    norm_end=common.datetime_str_to_lag(end,type)
    folder_path = config.model_production_folder if (type=="production") else config.model_consumption_folder
    model=sm.load(folder_path+common.get_latest_file(folder_path))
    result = model.predict(start=norm_start, end=norm_end, dynamic=False)
    log.add.info(f"ar model prediction type {type} created")
    return result

def _production_consumption_ratio(start, end):
    '''
    Calculates predicted ratio of renevables and energy consumption for given timeframe.

        Parameters:
        ----------

            start : str

            end : str

        Returns:
        ----------

            result : dataframe
                Single timeseries with predicted ratios.
    '''
    log.add.info(f"calculating production/consumption ratios for user input")
    production_prediction=_get_prediction(start, end, "production")
    consumption_prediction=_get_prediction(start, end, "consumption")
    result= production_prediction.divide(other=consumption_prediction).to_frame()
    log.add.info(f"production/consumption ratio from {start} to {end} calculated")
    return result

def _find_optimum(time_series, duration, start):
    '''
    Selects optimal time to start consuming energy within limitations.

        Parameters:
        ----------

            time_series : dataframe

            duration : int

            start : str
        
        Returns:
        ----------

            result : str
    '''
    log.add.info(f"selecting optimal starting time from timeseries")
    norm_duration=int(duration/15)
    max_cummulative_ratio=0
    optimal_period=0
    for period in range(time_series.size-norm_duration):
        subset_sum=sum(time_series.iloc[period: period+norm_duration].values)
        if subset_sum>max_cummulative_ratio:
            max_cummulative_ratio=subset_sum
            optimal_period=period
    result= common.lag_to_datetime(optimal_period, start)
    log.add.info(f"found optimal time from timeseries to start consuming energy: {result}")
    return result

def ar_prediction(start, end, duration):
    '''
    Returns ideal start time.

        Parameters:
        ----------
            
            start : str

            end : str

            duration : int
        
        Returns:
        ----------

            point_in_time : str
    '''
    time_series=_production_consumption_ratio(start, end)
    point_in_time =_find_optimum(time_series,duration, start)
    log.add.info(f"ar model prediction done")
    return point_in_time
