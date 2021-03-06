import pandas as pd
from random import randint, seed
from epi.helpers import common
from epi.prediction import predictor
from epi import logger as log
from epi import config


def _actual_prod_cons_ratio(start, end):
    """
    Calculates predicted ratio of renewables and energy consumption for given timeframe.

        Parameters:
        ----------

            start : str

            end : str

        Returns:
        ----------

            result : dataframe
                Single timeseries with predicted ratios.
    """
    dict = []
    for type in [config.p, config.c]:
        # pulls actual production and consumption for given timeframe
        dict.append(
            pd.read_pickle(f"{config.training_data_folder}{type}.pkl")[
                common.datetime_str_to_lag(start, type) : common.datetime_str_to_lag(
                    end, type
                )
                + 1
            ][type]
        )
    result = dict[0].divide(other=dict[1]).to_frame()
    log.add.info(
        f"calculated predicted production/consumption ratio between {start} - {end} "
    )
    return result


def _random_prediction(time_series, start, dur):
    """
    Selects a randome row from timeseries within limitations.

        Parameters:
        ----------

            time_series : dataframe
            
            start : str

            dur : int

        Returns:
        ----------

            result : str
                Selected datetime as string.
    """
    duration_in_lags = int(dur / 15)
    seed(time_series.size)
    optimal_period = randint(1, time_series.size - duration_in_lags)
    result = common.lag_to_datetime(optimal_period, start)
    log.add.info(f"generated randome prediction {result} later than {start}")
    return result


def run(start, end, dur):
    """
    Starts evaluation of test request.

        Parameters:
        ----------
            
            start : str

            end : str

            dur : int
        
        Returns:
        ----------

            best_start_time : str

            randome_prediction : str
    """
    time_series = _actual_prod_cons_ratio(start, end)
    result = (
        predictor.find_optimum(time_series, dur, start),
        _random_prediction(time_series, start, dur),
    )
    log.add.info("evaluation for testing purposes done")
    return result
