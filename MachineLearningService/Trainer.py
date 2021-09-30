import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import os
from wtforms.fields.core import Label
import Evaluator
import time


def parser(s):
    return datetime.strftime(s, "%d/%m/%Y %H:%M:%S")


def update_ar_model(file_path, start_intervall, end_intervall, start_lag, end_lag):
    # prepare training data
    df = pd.read_csv(file_path, index_col=0, parse_dates=[1], sep=",")
    col = "Consumption" if ("cons" in file_path.lower()) else "Production"
    data = df[col].apply(lambda y: int((y)))
    x = None

    #train for all 15m intervalls
    for intervall in range(start_intervall, end_intervall):
        target_rmse, target_lags = math.inf, 0
        train, test = data[:len(data)-intervall], data[len(data)-intervall:]

        #over all lags
        for lag in range(start_lag, end_lag):
            model = AutoReg(train, lags=lag, old_names=False).fit()
            pred = model.predict(
                start=len(train), end=len(data)-1, dynamic=False)
            if sqrt(mean_squared_error(test, pred)) < target_rmse:
                target_rmse = sqrt(mean_squared_error(test, pred))
                x = model

        #store best model
        output_folder_path = f"Ressources\Models\ModelsAutoRegression\ModelsAutoRegression{col}"
        model_name=str(intervall)+"_"+str(int(target_rmse))+".pickles"
        x.save(output_folder_path +"\\"+model_name)
        time.sleep(5)
        print(Evaluator.evaluate_model(file_path,intervall,model_name ))

if __name__ == "__main__":
    update_ar_model("Ressources\TrainingData\Production.csv", 1,3,3,4)
