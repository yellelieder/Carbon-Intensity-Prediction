import math
import os
from datetime import datetime, time, timedelta
from math import sqrt

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

def parser(s):
    return datetime.strftime(s, "%d/%m/%Y %H:%M:%S")


def evaluate_model(file_path, intervalls, model):
    '''returns True if the model performs better than taking a average'''

    #prepare training data
    df = pd.read_csv(file_path, index_col=0, parse_dates=[1], sep=",")
    col = "Consumption" if ("cons" in file_path.lower()) else "Production"
    data = df[col].apply(lambda y: int((y)))
    norm_start, norm_end = len(data)-intervalls, len(data)
    model = sm.load(f"Ressources\Models\ModelsAutoRegression\ModelsAutoRegression{col}\\{model}")
    predictions = model.predict(start=norm_start, end=norm_end, dynamic=False)
    test = data[len(data)-intervalls:]

    #calculate hourly mean for last year
    last_year = df[-(365*24*4):-1] 
    last_year_means = last_year.groupby(last_year['Date'].dt.hour).mean()

    #prepare visual outputs
    table = PrettyTable(["Time", 'Prediction', 'Target', "Mean", "Prediction/Target Dif",
                    "Mean/Target Dif", "Predition better then mean", "Dif-Dif"])
    dict = []

    #fill dict with values
    for key, value in test.items():
        prediction = predictions[key]
        target = value
        time = str(df.iloc[key, 0])
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
    #inspect_visual(results, rmse_prediction, rmse_mean,table)
    return rmse_prediction<rmse_mean

def inspect_visual(results, rmse_prediction, rmse_mean, t):
    results.plot(x="Time")
    plt.title("Prediction RMSE: " + str(int(rmse_prediction)) +" | Mean-Model RMSE: "+str(int(rmse_mean)))
    plt.xlabel('Time')
    plt.ylabel('MWh')
    plt.show()
    print(t)

if __name__ == "__main__":
    evaluate_model("Ressources\TrainingData\Production.csv", intervalls=36, model="16.pickles")
