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

def _get_predictions(start, end, type):
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
    norm_start=common.time_str_to_lag(start, type)
    norm_end=common.time_str_to_lag(end,type)
    folder_path = config.model_production_folder if (type=="production") else config.model_consumption_folder
    model=sm.load(folder_path+common.get_latest_file(folder_path))
    return model.predict(start=norm_start, end=norm_end, dynamic=False)

def _get_production_consumption_ratio(start, end):
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
    log.add.info(f"calculating production/consumption ratios for user input")
    production_prediction=_get_predictions(start, end, "production")
    consumption_prediction=_get_predictions(start, end, "consumption")
    return production_prediction.divide(other=consumption_prediction).to_frame()

def _find_optimum(time_series, duration, start):
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
    log.add.info(f"selecting optimal starting time from timeseries")
    norm_duration=int(duration/15)
    max_cummulative_ratio=0
    optimal_period=0
    for period in range(time_series.size-norm_duration):
        subset_sum=sum(time_series.iloc[period: period+norm_duration].values)
        if subset_sum>max_cummulative_ratio:
            max_cummulative_ratio=subset_sum
            optimal_period=period
    return common.lag_to_datetime(optimal_period, start)

def ar_prediction(start, end, duration):
    time_series=_get_production_consumption_ratio(start, end)
    point_in_time =_find_optimum(time_series,duration, start)
    log.add.info(f"prediction successful")
    return point_in_time
