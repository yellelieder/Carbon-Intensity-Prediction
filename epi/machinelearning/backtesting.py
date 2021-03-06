from datetime import datetime
from math import sqrt
from epi.helpers import common
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from prettytable import PrettyTable
from sklearn.metrics import mean_squared_error
from epi import config
from epi import logger as log


def parser(datetime_object):
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
    return datetime.strftime(datetime_object, config.dateformat)


def evaluate_model(training_data_file_path, intervalls, model):
    """
    Returns True if the input model performs better than taking a average.

        Parameters:
        ----------

            training_data_file_path : str
                File paht where training date is located.

            intervalls : int 
                Number of intervalls to be used for validation/rmse.

            model : str
                Name of the file that contains the model to be evaluated.

        Returns:
        ----------

            result : bool
                True is model outperforms a standard mean model.
    """
    try:
        df = pd.read_csv(training_data_file_path, index_col=0, parse_dates=[1], sep=",")
    except FileNotFoundError as exception:
        common.print_fnf(training_data_file_path, exception)
    col = config.c if ("cons" in training_data_file_path.lower()) else config.p
    data = df[col].apply(lambda y: int((y)))
    norm_start, norm_end = len(data) - intervalls, len(data)
    model = sm.load(
        f"{config.model_folder}ModelsAutoRegression{col}{config.slash}{model}"
    )
    predictions = model.predict(start=norm_start, end=norm_end, dynamic=False)
    test = data[len(data) - intervalls :]

    # calculate hourly mean for last year
    last_year = df[-(365 * 24 * 4) : -1]
    last_year_means = last_year.groupby(last_year["Date"].dt.hour).mean()
    log.add.info("calculated yearly hourly mean in given dataset")

    # prepare visual outputs
    table = PrettyTable(
        [
            "Time",
            "Prediction",
            "Target",
            "Mean",
            "Prediction/Target Dif",
            "Mean/Target Dif",
            "Predition better then mean",
            "Dif-Dif",
        ]
    )
    dict = []

    # fill dict with values
    for key, value in test.items():
        prediction = predictions[key]
        target = value
        time = parser(datetime.strptime(str(df.iloc[key, 0]), "%Y-%m-%d %H:%M:%S"))
        
        hour = int((time.split(" ")[1]).split(":")[0])
        mean = int(last_year_means.iloc[hour, 0])
        dict.append(
            {"Time": time, "Prediction": prediction, "Target": target, "Mean": mean,}
        )

        table.add_row(
            [
                time,
                prediction,
                target,
                mean,
                int(abs(prediction - target)),
                int(abs(mean - prediction)),
                int(abs(prediction - target)) < int(abs(mean - prediction)),
                abs(int(abs(prediction - target)) - int(abs(mean - prediction))),
            ]
        )
    results = pd.DataFrame(dict)

    # evaluate
    rmse_prediction = sqrt(mean_squared_error(test, predictions[0:intervalls]))
    rmse_mean = sqrt(mean_squared_error(test, results["Mean"]))

    # uncomment to see graphs and tables:
    # _inspect_visual(results, rmse_prediction, rmse_mean,table, col)
    result = rmse_prediction < rmse_mean
    log.add.info(
        f"model evaluation successfull, intervalls: {intervalls}, model: {model}, performs better than taking a mean: {result}"
    )
    return result


# activate in line 120
def _inspect_visual(results, rmse_prediction, rmse_mean, table, column_name):
    """
    Plots graphs for model evaluation and prints table with acutal numbers.

        Parameters:
        ----------

            results : dataframe
                Containing all values for plotting.

            rmse_prediction : float

            rmse_mean : float

            table : PrettyTable
                Table with relevant numbers.

            comumn_name : str
                Type of the date (Production/Consumption).

        Returns:
        ----------

            None : mathplotlib Plot and Table to consol.
    """
    results.plot(x="Time")
    plt.title(
        f"Energy {column_name} | Prediction RMSE: "
        + str(int(rmse_prediction))
        + " | Mean-Model RMSE: "
        + str(int(rmse_mean))
    )
    plt.xlabel("Time")
    plt.ylabel("MWh")
    plt.show()
    print(table)
    log.add.info(
        f"displayed visual evaluation of {column_name} prediction with rmse: {rmse_prediction}"
    )


# run this for manual evaluation and visualisation of the models
if __name__ == "__main__":
    evaluate_model(
        "Ressources{config.slash}TrainingData{config.slash}Production.csv",
        intervalls=7 * 96,
        model="3.pickles",
    )
    evaluate_model(
        "Ressources{config.slash}TrainingData{config.slash}Consumption.csv",
        intervalls=7 * 96,
        model="4.pickles",
    )
