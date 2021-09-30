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

PRODUCTION_DATA_FOLDER_PATH = "Ressources\\Training Data Production\\"
PRODUCTION_MODEL_FOLDER_PATH = "Ressources\\Models Production\\"
TIME_STAMP = re.sub(
    '[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def parser(s):
    return datetime.strftime(s, "%d/%m/%Y %H:%M:%S")

def evaluate_model(file_path):
    # df.to_pickle("MachineLearningService\data.pkl")
    df = pd.read_pickle("MachineLearningService\data.pkl")
    col = "Consumption" if ("cons" in file_path.lower()) else "Production"
    data = df[col]
    data = data.apply(lambda y: int((y)))

    intervalls = 96
    norm_start = len(data)-intervalls
    norm_end = len(data)
    model = sm.load(
        r"Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionProduction\16.pickles")
    pred = model.predict(start=norm_start, end=norm_end, dynamic=False)
    df["Date"] = pd.to_datetime(df["Date"])
    test = data[len(data)-intervalls:]
    rmse_prediction = str(
        int(sqrt(mean_squared_error(test, pred[0:intervalls]))))
    ly = pd.read_pickle("MachineLearningService\last_year.pkl")
    #ly=pd.read_csv(f"Ressources\TrainingData\{col}.csv", index_col=0,skiprows=range(1, 175392), parse_dates=[1],sep=",")
    ly['Date'] = pd.to_datetime(ly['Date'])
    mea = ly.groupby(ly['Date'].dt.hour).mean()
    # ly.to_pickle("MachineLearningService\last_year.pkl")
    t = PrettyTable(["Time", 'Prediction', 'Target', "Mean", "Prediction/Target Dif",
                    "Mean/Target Dif", "Predition better then mean", "Dif-Dif"])
    d = []
    for i, v in test.items():
        pre = pred[i]
        tar = v
        time = str(df.iloc[i, 0])
        hour = int((time.split(" ")[1]).split(":")[0])
        m = int(mea.iloc[hour, 0])
        d.append({"Time": time, 'Prediction': pre,
                  'Target': tar,
                  "Mean": m,
                  }
                 )
        t.add_row([time, pre, tar,  m,  int(abs(pre-tar)),  int(abs(m-pre)),
                  int(abs(pre-tar)) < int(abs(m-pre)), abs(int(abs(pre-tar))-int(abs(m-pre)))])
    results = pd.DataFrame(d)
    rmse_mean = str(int(sqrt(mean_squared_error(test, results["Mean"]))))
    results.plot(x="Time")
    plt.title("Prediction RMSE: " + rmse_prediction +
              " | Mean-Model RMSE: "+rmse_mean)
    plt.xlabel('Uhrzeit')
    plt.ylabel('MWh')
    #plt.show()
    #print(t)


if __name__ == "__main__":
    evaluate_model("Ressources\TrainingData\Production.csv")
