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
from app.machinelearning import backtesting
import time
import csv  
import config
import logger as log


def parser(s):
    return datetime.strftime(s, config.dateformat)

def _get_free_id():
    df=pd.read_csv("Ressources\Models\Models.csv",sep=",", dtype={
                     'ID': int,
                     "Type":str, 
                     "intervalls for training":str, 
                     "startdate":str, 
                     "enddate":str, 
                     "lags":str, 
                     "lag_start":str,
                     "lag_end":str,
                     "rmse":str, 
                     "evaluationresult":str
                 })
    max= df.loc[df['ID'].idxmax()][0]
    return int(max)+1


def update_ar_model(type, intervall, start_lag, end_lag, start_skip, end_skip):
    # prepare training data  
    file_path="Ressources\TrainingData\Production.csv" if type=="1" else "Ressources\TrainingData\Consumption.csv"
    df = pd.read_csv(file_path, index_col=0,parse_dates=[1], skiprows=range(start_skip, end_skip), sep=",")    
    column_name = "Consumption" if ("cons" in file_path.lower()) else "Production"
    data = df[column_name].apply(lambda y: int((y)))
    target_model = None

    target_rmse, target_lags = math.inf, 0
    train, test = data[:len(data)-intervall], data[len(data)-intervall:]

    for lag in range(start_lag, end_lag):
        print("Lag: ", lag)
        model = AutoReg(train, lags=lag, old_names=False).fit()
        pred = model.predict(
            start=len(train), end=len(data)-1, dynamic=False)
        if sqrt(mean_squared_error(test, pred)) < target_rmse:
            target_rmse = sqrt(mean_squared_error(test, pred))
            target_model = model
            target_lags=lag

    #store best model
    output_folder_path = f"{config.model_folder}ModelsAutoRegression{column_name}"
    model_id =_get_free_id()
    model_name=str(model_id)+".pickles"
    target_model.save(output_folder_path +"\\"+model_name)
    time.sleep(5)
    evaluation_result=backtesting.evaluate_model(file_path,intervall,model_name)
    
    csv_output = [str(model_id),column_name,str(intervall),str(df.iloc[0,0]).split(" ")[0],str(df.iloc[start_skip-1,0]).split(" ")[0],str(target_lags),str(start_lag), str(end_lag), int(target_rmse), str(evaluation_result) ]
    # with open('Ressources\Models\Models.csv', 'a', encoding='UTF8', newline='') as f:
    #     f.write(csv_output)
    with open(r'Ressources\Models\Models.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(csv_output)

if __name__ == "__main__":
    #update_ar_model("Ressources\TrainingData\Production.csv", 4*96,1,288+100,227805, -1)
    update_ar_model(type="Ressources\TrainingData\Production.csv",intervall=5*96,start_lag= 1,end_lag= 680,start_skip= 227805,end_skip= -1)
    update_ar_model(type="Ressources\TrainingData\Consumption.csv",intervall=5*96,start_lag= 1,end_lag= 680,start_skip= 227805,end_skip= -1)
