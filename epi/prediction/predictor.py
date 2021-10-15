import statsmodels.api as sm
from epi.helpers import common
from epi import config
from epi import logger as log


def _get_prediction(start, end, type):
    """
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
    """
    norm_start = common.datetime_str_to_lag(start, type)
    norm_end = common.datetime_str_to_lag(end, type)
    folder_path = (
        config.model_production_folder
        if (type == "production")
        else config.model_consumption_folder
    )
    model = sm.load(folder_path + common.get_latest_file(folder_path))
    result = model.predict(start=norm_start, end=norm_end, dynamic=False)
    log.add.info(f"ar model prediction type {type} created")
    return result


def _production_consumption_ratio_prediction(start, end):
    """
    Calculates predicted ratio of renevables and energy consumption for given timeframe.

        Parameters:
        ----------

            start : str

            end : str

        Returns:
        ----------

            result : dataframe
                Single timeseries with predicted ratios.
    """
    production_prediction = _get_prediction(start, end, "production")
    consumption_prediction = _get_prediction(start, end, "consumption")
    result = production_prediction.divide(other=consumption_prediction).to_frame()
    log.add.info(f"production/consumption ratio from {start} to {end} calculated")
    return result


def find_optimum(time_series, duration, start):
    """
    Selects optimal time to start consuming energy within limitations.

        Parameters:
        ----------

            time_series : dataframe

            duration : int

            start : str
        
        Returns:
        ----------

            result : str
    """
    duration_in_lags = int(duration / 15)
    max_cummulative_ratio, optimal_period = 0, 0
    for period in range(time_series.size - duration_in_lags):
        subset_sum = sum(time_series.iloc[period : period + duration_in_lags].values)
        if subset_sum > max_cummulative_ratio:
            max_cummulative_ratio = subset_sum
            optimal_period = period
    result = common.lag_to_datetime(optimal_period, start)
    log.add.info(
        f"found best start time ({result}) after {start} with duration {duration}"
    )
    return result


def ar_prediction(start, end, duration):
    """
    Returns ideal start time.

        Parameters:
        ----------
            
            start : str

            end : str

            duration : int
        
        Returns:
        ----------

            point_in_time : str
    """
    time_series = _production_consumption_ratio_prediction(start, end)
    point_in_time = find_optimum(time_series, duration, start)
    log.add.info(f"ar model prediction done")
    return point_in_time
