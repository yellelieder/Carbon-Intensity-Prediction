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

PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
LAGS=672
NO_OF_DAYS_TO_PREDICT=3

TIME_STAMP = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("autoregression.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

def getLatestFile(dir):
    '''
    Returns last file form folder by alphabetical order.

        Parameters:
        ----------
        dir : str
            Folder to search from.

        Returns:
        ----------
        file_name : str
            Name of the last file from the folder in alphabetical order.
    '''
    return sorted(os.listdir(dir)).pop()

def parser(s):
    '''
    asdf

        Parameters:
        ----------
        asdf : str
            asdf

        Returns:
        ----------
        asdf : int
            asdf
    '''
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

def train_ar_model(file_path):
    '''
    asdf

        Parameters:
        ----------
        asdf : str
            asdf

        Returns:
        ----------
        asdf : int
            asdf
    '''
    log.info(f"training ar model with data from file: {file_path}")
    df=pd.read_csv(file_path, index_col=0, parse_dates=[1],sep=",")
    col= "Consumption" if ("cons" in file_path.lower()) else "Production"
    data=df[col]
    data=data.apply(lambda y: int((y)))
    analyze_training_data(df, col)
    predition_lenght = NO_OF_DAYS_TO_PREDICT*96
    train=data[:len(data)-predition_lenght]
    test=data[len(data)-predition_lenght:]
    model=AutoReg(train, lags=LAGS).fit()
    print(model.summary())
    output_folder_path= "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionConsumption" if ("cons" in file_path.lower()) else "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionProduction"
    model.save(output_folder_path+"\AR_"+col+"_"+TIME_STAMP+".pickles")
    pred=model.predict(start=len(train), end=len(data)-1, dynamic=False)
    plt.plot(pred)
    plt.plot(test, color="red")
    plt.show()
    rmse=sqrt(mean_squared_error(test,pred))
    print(rmse)

def analyze_training_data(df, col):
    '''
    asdf

        Parameters:
        ----------
        asdf : str
            asdf

        Returns:
        ----------
        asdf : int
            asdf
    '''
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

if __name__ == "__main__":
    start = time.time()
    print("start..\n")
    train_ar_model("Ressources\TrainingData\Production.csv")
    print("end\n","duration: ", time.time()-start)
    


