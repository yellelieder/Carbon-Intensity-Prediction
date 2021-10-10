import math
import os
from datetime import datetime, time, timedelta
from math import sqrt
from app.helpers import common

import matplotlib.pyplot as plt
import pandas as pd
import regex as re
import statsmodels.api as sm
from prettytable import PrettyTable
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller
from wtforms.fields.core import Label
import config
import logger as log

def parser(s):
    return datetime.strftime(s, config.dateformat)


def evaluate_model(training_data_file_path, intervalls, model):
    '''returns True if the model performs better than taking a average'''
    #prepare training data
    try:
        df = pd.read_csv(training_data_file_path, index_col=0, parse_dates=[1], sep=",")
    except FileNotFoundError as exception:
        common.print_fnf(training_data_file_path, exception)
    col = config.c if ("cons" in training_data_file_path.lower()) else config.p
    data = df[col].apply(lambda y: int((y)))
    norm_start, norm_end = len(data)-intervalls, len(data)
    model = sm.load(f"{config.model_folder}{col}\\{model}")
    predictions = model.predict(start=norm_start, end=norm_end, dynamic=False)
    test = data[len(data)-intervalls:]

    #calculate hourly mean for last year
    last_year = df[-(365*24*4):-1] 
    last_year_means = last_year.groupby(last_year['Date'].dt.hour).mean()
    log.add.info(f"calculated yearly hourly mean in given dataset")

    #prepare visual outputs
    table = PrettyTable(["Time", 'Prediction', 'Target', "Mean", "Prediction/Target Dif",
                    "Mean/Target Dif", "Predition better then mean", "Dif-Dif"])
    dict = []

    #fill dict with values
    for key, value in test.items():
        prediction = predictions[key]
        target = value
        time = parser(datetime.strptime(str(df.iloc[key, 0]), "%Y-%m-%d %H:%M:%S"))
        print(time)
        hour = int((time.split(" ")[1]).split(":")[0])
        mean = int(last_year_means.iloc[hour, 0])
        dict.append({"Time": time, 'Prediction': prediction, 'Target': target, "Mean": mean,})

        table.add_row([time, prediction, target,  mean,  int(abs(prediction-target)),  int(abs(mean-prediction)),
                  int(abs(prediction-target)) < int(abs(mean-prediction)), abs(int(abs(prediction-target))-int(abs(mean-prediction)))])
    results = pd.DataFrame(dict)

    #evaluate
    rmse_prediction = sqrt(mean_squared_error(test, predictions[0:intervalls]))
    rmse_mean = sqrt(mean_squared_error(test, results["Mean"]))

    #uncomment to see graphs and tables:
    #_inspect_visual(results, rmse_prediction, rmse_mean,table, col)
    result =rmse_prediction<rmse_mean
    log.add.info(f"model evaluation successfull, intervalls: {intervalls}, model: {model}, performs better than taking a mean: {result}")
    return rmse_prediction<rmse_mean

def _inspect_visual(results, rmse_prediction, rmse_mean, table, column_name):
    results.plot(x="Time")
    plt.title(f"Energy {column_name} | Prediction RMSE: " + str(int(rmse_prediction)) +" | Mean-Model RMSE: "+str(int(rmse_mean)))
    plt.xlabel('Time')
    plt.ylabel('MWh')
    plt.show()
    print(table)
    log.add.info(f"displayed visual evaluation of {column_name} prediction with rmse: {rmse_prediction}")

#run this for manual evaluation and visualisation of the models, uncomment line 61
if __name__ == "__main__":
    evaluate_model("Ressources\TrainingData\Production.csv", intervalls=7*96, model="3.pickles")
    evaluate_model("Ressources\TrainingData\Consumption.csv", intervalls=7*96, model="4.pickles")
