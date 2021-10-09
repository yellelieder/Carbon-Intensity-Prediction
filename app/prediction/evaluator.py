from datetime import datetime, timedelta
import pandas as pd
from random import randint, seed
from app.helpers import common
import logger as log
import config

def _production_consumption_ratio(start, end):
    dict=[]
    for type in ["Production", "Consumption"]:
        dict.append(pd.read_pickle(f"{config.training_data_folder}{type}.pkl")[common.datetime_str_to_lag(start,type):common.datetime_str_to_lag(end,type)+1][type])
    return dict[0].divide(other=dict[1]).to_frame()

def _best_start_time(time_series, duration, start):
    duration_in_lags=int(duration/15)
    max_cummulative_ratio,optimal_period=0,0
    for period in range(time_series.size-duration_in_lags):
        subset_sum=sum(time_series.iloc[period: period+duration_in_lags].values)
        if subset_sum>max_cummulative_ratio:
            max_cummulative_ratio=subset_sum
            optimal_period=period
    return common.lag_to_datetime(optimal_period, start)

def _random_prediction(time_series, start, dur):
    duration_in_lags=int(dur/15)
    seed(time_series.size)
    optimal_period=randint(1, time_series.size-duration_in_lags)
    return common.lag_to_datetime(optimal_period, start)


def run(start, end, dur):
    time_series = _production_consumption_ratio(start, end)
    log.add.info(f"runtime evaluation done")
    return _best_start_time(time_series, dur,start), _random_prediction(time_series, start, dur)