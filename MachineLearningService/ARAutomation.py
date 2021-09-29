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

PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
TIME_STAMP = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def parser(s):
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

def update_ar_model(file_path):
    #todo: find out how to rename x labels
    df=pd.read_csv(file_path, index_col=0, parse_dates=[1],sep=",")
    col= "Consumption" if ("cons" in file_path.lower()) else "Production"
    data=df[col]
    data=data.apply(lambda y: int((y)))
    intervalls = 96*3
    train, test=data[:len(data)-intervalls], data[len(data)-intervalls:]
    target_rmse, target_lags, optimal_prediction = math.inf, 0, None
    change =0
    for i in range(10):
        print("Iteration: ",i)
        pred=AutoReg(train, lags=i).fit().predict(start=len(train), end=len(data)-1, dynamic=False)
        if sqrt(mean_squared_error(test,pred))<target_rmse:
            change +=1
            print("Change: ",change)
            target_rmse=sqrt(mean_squared_error(test,pred))
            target_lags=i
            optimal_prediction=pred
            print("tmp lags: ",target_lags," with RMSE: ", target_rmse)
    df['Date'] = pd.to_datetime(df['Date'])
    #todo: try if plot works
    #plt.plot(df.groupby(df['Date'].dt.hour).mean(), color="green", label="Yearly Mean")
    plt.plot(optimal_prediction, label="Prediction")
    plt.plot(test, color="red", label="Target")
    plt.title("Prediction Evaluation")   
    plt.xlabel("15 min. time frames")
    plt.ylabel("Energy in MWh")
    plt.legend()
    plt.show()

    print("target lags: ",target_lags," with RMSE: ", target_rmse)

if __name__ == "__main__":
    update_ar_model("Ressources\TrainingData\Production.csv")

    


