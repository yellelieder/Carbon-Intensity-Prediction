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


PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def getLatestFile(dir):
    return sorted(os.listdir(dir)).pop()

def parser(s):
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

def train_ar_model(file_path):
    df=pd.read_csv(file_path, index_col=0, parse_dates=[1],sep=",")
    col= "Consumption" if ("cons" in file_path.lower()) else "Production"
    df[col]=df[col].apply(lambda y: int((y)))
    dftest=adfuller(df[col], autolag="AIC")
    print("1. ADF: ", dftest[0])
    print("2. P-Value: ", dftest[1])
    print("\tshould be: <0.5")
    print("3. Num Of Lags: ", dftest[2])
    print("4. Number Of Observations Used For ADF Regression and Critical Values Calculation: ", dftest[3])
    print("5. Critical Values: ")
    for key, val in dftest[4].items():
        print("\t", key, ": ",val)

    '''print("\tpearson correlation coefficient: ")
    pacf=plot_pacf(df[col], lags=35040)
    plt.show()
    acf=plot_acf(df[col], lags=35040)
    plt.show()'''

    x=df[col]
    no_of_days_to_predict = 14*96
    train=x[:len(x)-no_of_days_to_predict]
    test=x[len(x)-no_of_days_to_predict:]
    model=AutoReg(train, lags=10).fit()
    print(model.summary())
    output_folder_path= "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionConsumption" if ("cons" in file_path.lower()) else "Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionProduction"
    model.save(output_folder_path+"\AR_"+col+"_"+timeStamp+".pickles")
    pred=model.predict(start=len(train), end=len(x)-1, dynamic=False)
    plt.plot(pred)
    plt.plot(test, color="red")
    plt.show()
    rmse=sqrt(mean_squared_error(test,pred))
    print(rmse)

if __name__ == "__main__":
    start = time.time()
    print("start..\n")
    train_ar_model("Ressources\TrainingData\Consumption.csv")
    print("end\n","duration: ", time.time()-start)
    
    
    #p should still be lower than 0.5
    


