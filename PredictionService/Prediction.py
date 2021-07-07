
import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
import StaticMain
PRODUCTION_MODEL_FOLDER_PATH="Ressources\\Models Production\\"
CONSUMPTION_MODEL_FOLDER_PATH ="Ressources\\Models Consumption\\"


#x=df_production["Renevables"]
#no_of_days_to_predict = 14
#train=x[:len(x)-no_of_days_to_predict]
#test=x[len(x)-no_of_days_to_predict:]
model=sm.load(PRODUCTION_MODEL_FOLDER_PATH+StaticMain().getLatestFile(PRODUCTION_MODEL_FOLDER_PATH))
#p should still be lower than 0.5
print(model.summary())
pred=model.predict(start=len(train), end=len(x)-1, dynamic=False)
plt.plot(pred)
plt.plot(test, color="red")
plt.show()
rmse=sqrt(mean_squared_error(test,pred))
print(rmse)