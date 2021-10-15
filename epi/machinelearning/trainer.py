import pandas as pd
from datetime import datetime
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
from webdriver_manager.utils import File
from wtforms.fields.core import Label
from epi.machinelearning import backtesting
import time
import csv
from epi import config
from epi import logger as log
from epi.helpers import common


def parser(s):
    """
    Converts datetime object to string dd/mm/yyyy hh:mm:ss.

    Redundant to common.datetime_to_str() but must be located in this file.
        Implicitly used in evaluate_model() -> parse_dates.

        Parameters:
        ----------

            datetime_object : datetime

        Returns:
        ----------

            date_time : str
    """
    return datetime.strftime(s, config.dateformat)


def _get_free_id():
    """
    Returns next free model ID.

        Parameters:
        ----------

            None

        Returns:
        ----------

            result : int
    """
    try:
        df = pd.read_csv(
            config.training_log_file,
            sep=",",
            dtype={
                "ID": int,
                "Type": str,
                "intervalls for training": str,
                "startdate": str,
                "enddate": str,
                "lags": str,
                "lag_start": str,
                "lag_end": str,
                "rmse": str,
                "evaluationresult": str,
            },
        )
    except FileNotFoundError as exception:
        common.print_fnf(config.training_log_file, exception)
    max = df.loc[df["ID"].idxmax()][0]
    result = int(max) + 1
    log.add.info(f"returned next free id ({result}) in {config.training_log_file}")
    return result


def update_ar_model(type, intervall, start_lag, end_lag, start_skip) -> None:
    """
    Returns next free model ID.

        Parameters:
        ----------

            type : str
                Data type 1 = Production, 2 = Consumption
            
            intervall : int
                Number of lags to be excluded from training / included in test set.
            
            start_lag : int
                Minimum number of lags to be concidered for AR-Model training.
            
            end_lag : int
                Maximum number of lags to be concidered for AR-Model training.
            
            start_skip :int 
                First row to be excluded from training AND testing set.

        Returns:
        ----------

            None : Persists model as [id].pickles and training log as models.csv.
    """
    # prepare training data
    file_path = (
        config.training_data_folder
        + (config.p if type == config.p_id else config.c)
        + ".csv"
    )
    df = pd.read_csv(
        file_path, index_col=0, parse_dates=[1], skiprows=range(start_skip, -1), sep=","
    )
    column_name = config.c if type == config.c_id else config.p
    data = df[column_name].apply(lambda y: int((y)))
    target_model = None
    target_rmse, target_lags = math.inf, 0
    train, test = data[: len(data) - intervall], data[len(data) - intervall :]
    # train and evaluate model for each given lag
    for lag in range(start_lag, end_lag):
        model = AutoReg(train, lags=lag, old_names=False).fit()
        pred = model.predict(start=len(train), end=len(data) - 1, dynamic=False)
        # persist if model outperforms
        if sqrt(mean_squared_error(test, pred)) < target_rmse:
            target_rmse = sqrt(mean_squared_error(test, pred))
            target_model = model
            target_lags = lag

    # store best model
    output_folder_path = f"{config.model_folder}ModelsAutoRegression{column_name}"
    model_id = _get_free_id()
    model_name = str(model_id) + ".pickles"
    target_model.save(output_folder_path + config.slash + model_name)
    log.add.info(f"persisted model of type {type} with name: {model_name}")
    time.sleep(5)
    evaluation_result = backtesting.evaluate_model(file_path, intervall, model_name)
    # write details to training log
    csv_output = [
        str(model_id),
        column_name,
        str(intervall),
        str(df.iloc[0, 0]).split(" ")[0],
        str(df.iloc[start_skip - 1, 0]).split(" ")[0],
        str(target_lags),
        str(start_lag),
        str(end_lag),
        int(target_rmse),
        str(evaluation_result),
    ]
    try:
        with open(config.training_log_file, "a") as f:
            writer = csv.writer(f)
            writer.writerow(csv_output)
            log.add.info(f"documented model creation in {config.training_log_file}")
    except FileNotFoundError as exception:
        common.print_fnf(config.training_log_file, exception)
