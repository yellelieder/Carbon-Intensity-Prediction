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
import StaticMain

PRODUCTION_DATA_FOLDER_PATH="Ressources\\Training Data Production\\"
PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))



def parser(s):
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

if __name__ == "__main__":
    df_production=pd.read_csv(PRODUCTION_DATA_FOLDER_PATH+StaticMain().getLatestFile(PRODUCTION_DATA_FOLDER_PATH), index_col=0, parse_dates=[1],sep=",")
    #plotting the production
    plt.plot(df_production["Date"],df_production["Renevables"])
    plt.ylabel("Production")
    plt.xlabel("Time")
    plt.show()
    #checking that autoregression can be done on this data set, due to statistical limitations
    dftest=adfuller(df_production["Renevables"], autolag="AIC")
    print("1. ADF: ", dftest[0])
    #if p is high (>0.5), timeseries is not stationary, but it should be
    print("2. P-Value: ", dftest[1])
    print("3. Num Of Lags: ", dftest[2])
    print("4. Number Of Observations Used For ADF Regression and Critical Values Calculation: ", dftest[3])
    print("5. Critical Values: ")
    for key, val in dftest[4].items():
        print("\t", key, ": ",val)
    print(df_production)
    #check how many past values should be concidered
    #partial autocorrelation k

    #shows how correlated different timeperiod values are
    #contains only direct effects
    pacf=plot_pacf(df_production["Renevables"], lags=1344)
    #x axis shows how many periods (15 min) the correlation is back, 96 periods is one day, whole df has 525.600 periods
    plt.show()
    #1344 is for the past two weeks
    pacf=plot_acf(df_production["Renevables"], lags=1344)
    plt.show()
    #define training set
    x=df_production["Renevables"]
    print(x)
    no_of_days_to_predict = 14
    train=x[:len(x)-no_of_days_to_predict]
    #test=x[len(x)-no_of_days_to_predict:]
    model=AutoReg(train, lags=192).fit()

    model.save(PRODUCTION_MODEL_FOLDER_PATH+"AR_Production_"+timeStamp+".pickles")
    
    #p should still be lower than 0.5
    '''print(model.summary())
    pred=model.predict(start=len(train), end=len(x)-1, dynamic=False)
    plt.plot(pred)
    plt.plot(test, color="red")
    plt.show()
    rmse=sqrt(mean_squared_error(test,pred))
    print(rmse)'''


