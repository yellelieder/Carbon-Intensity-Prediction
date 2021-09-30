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
import os
import time
import logging

from wtforms.fields.core import Label

PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
NO_OF_DAYS_TO_PREDICT=1
LAGS=96*3
TIME_STAMP = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

def get_latest_file(dir):
    return sorted(os.listdir(dir)).pop()

def parser(s):
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

def update_ar_model(file_path):
    log.info(f"training ar model with data from file: {file_path}")
    df=pd.read_csv(file_path, index_col=1, parse_dates=[1],sep=",")
    col= "Consumption" if ("cons" in file_path.lower()) else "Production"
    data=df[col]
    data=data.apply(lambda y: int((y)))
    '''analyze_training_data(df, col)'''
    intervalls = NO_OF_DAYS_TO_PREDICT*96
    train=data[:len(data)-intervalls]
    model=AutoReg(train, lags=LAGS).fit()
    test=data[len(data)-intervalls:]
    pred=model.predict(start=len(train), end=len(data)-1, dynamic=False)
    #print(model.summary())
    plt.plot(pred, label="Prediction")
    plt.plot(test, color="red", label="Target")
    plt.title("Prediction Evaluation")   
    plt.xlabel("15 min. time frames")
    plt.ylabel("Energy in MWh")
    #plt.ylim(ymin=0)
    #plt.xlim(xmin=0)
    plt.legend()
    plt.show()
    rmse=sqrt(mean_squared_error(test,pred))
    output_folder_path= "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionConsumption" if ("cons" in file_path.lower()) else "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionProduction"
    model.save(output_folder_path+"\AR_"+col+"_"+TIME_STAMP+"_Lags_"+str(LAGS)+"_RMSE_"+str(rmse)+"_.pickles")
    

def analyze_training_data(df, col):
    log.info(f"creating visual analyziz for auto regression training")
    dftest=adfuller(df[col], autolag="AIC")
    print("1. ADF: ", dftest[0])
    print("2. P-Value: ", dftest[1])
    print("\tshould be: <0.5")
    print("3. Num Of Lags: ", dftest[2])
    print("4. Number Of Observations Used For ADF Regression and Critical Values Calculation: ", dftest[3])
    print("5. Critical Values: ")
    for key, val in dftest[4].items():
        print("\t", key, ": ",val)
    print("\npearson correlation coefficient.. ")
    pacf=plot_pacf(df[col], lags=LAGS)
    plt.show()
    print("\npreparing auto correlation plot..")
    acf=plot_acf(df[col], lags=LAGS)
    plt.show()

#for manual testing
if __name__ == "__main__":
    start = time.time()
    print("start..\n")
    update_ar_model("Ressources\TrainingData\Production.csv")
    print("end\n","duration: ", time.time()-start)
    


