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
    intervall_range_start=21 #1x = 15m prediction intervall
    intervall_range_end=96*7 #96x = 24h
    lag_range_start=1#No.of intervalls to look back at for prediction
    lag_range_end=100
    model_id=1
    x=None
    #usually one more loop for each sub-trainin set
    for intervalls in range (intervall_range_start,intervall_range_end):
        target_rmse, target_lags, optimal_prediction, target_intervalls = math.inf, 0, None,1
        train, test=data[:len(data)-intervalls], data[len(data)-intervalls:]
        for i in range(lag_range_start, lag_range_end):
            model = AutoReg(train, lags=i, old_names=False).fit()
            x=model
            pred=model.predict(start=len(train), end=len(data)-1, dynamic=False)
            if sqrt(mean_squared_error(test,pred))<target_rmse:
                target_rmse=sqrt(mean_squared_error(test,pred))
                target_lags=i+1
                optimal_prediction=pred
        output_folder_path= "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionConsumption" if ("cons" in file_path.lower()) else "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionProduction"
        x.save(output_folder_path+ "\\"+str(model_id) + ".pickles")
        with open(r"MachineLearningService\best_lags.txt", "a") as f:
            f.write("ID: "+str(model_id)+" | Intervall: "+ str(intervalls)+" | Lag: "+str(target_lags)+" | RMSE: "+ str(int(target_rmse))+" | Tested Lag Range: "+ str(lag_range_start)+" - "+str(lag_range_end)+"\n")
        model_id+=1
    df['Date'] = pd.to_datetime(df['Date'])
    #todo: try if plot works
    #plt.plot(df.groupby(df['Date'].dt.hour).mean(), color="green", label="Yearly Mean")
    plt.plot(optimal_prediction, label="Prediction")
    plt.plot(test, color="red", label="Target")
    plt.title("Prediction Evaluation")   
    plt.xlabel("15 min. time frames")
    plt.ylabel("Energy in MWh")
    plt.legend()
    #plt.show()
    print("..done")



if __name__ == "__main__":
    update_ar_model("Ressources\TrainingData\Production.csv")

    


