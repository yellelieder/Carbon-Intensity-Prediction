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
import numpy as np



def get_latest_file(dir):
    return sorted(os.listdir(dir)).pop()

def parser(s):
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

def update_ar_model():
    last_year_production=pd.read_csv("Ressources\TrainingData\Production.csv", index_col=0,skiprows=range(1, 175392), parse_dates=[1],sep=",")
    last_year_production['Date'] = pd.to_datetime(last_year_production['Date'])

    last_year_consumption=pd.read_csv("Ressources\TrainingData\Consumption.csv", index_col=0,skiprows=range(1, 175392), parse_dates=[1],sep=",")
    last_year_consumption['Date'] = pd.to_datetime(last_year_consumption['Date'])

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
    print(type(last_year_production))
    weekday_production_mean = last_year_production.groupby(last_year_production['Date'].dt.day_name()).mean().reindex(days)
    weekday_consumption_mean = last_year_consumption.groupby(last_year_consumption['Date'].dt.day_name()).mean().reindex(days)
    hour_prodction_mean = last_year_production.groupby(last_year_production['Date'].dt.hour).mean()
    hour_consumption_mean = last_year_consumption.groupby(last_year_consumption['Date'].dt.hour).mean()

    print(weekday_production_mean)
    print(weekday_consumption_mean)
    print(hour_prodction_mean)
    print(hour_consumption_mean)

    plt.title("last year weekly average")   
    plt.plot(weekday_production_mean, label = "Production")
    plt.plot(weekday_consumption_mean, label = "Consumption")
    plt.xlabel("weekyday")
    plt.ylabel("Energy in MWh")
    plt.legend()
    plt.show()

    plt.title("last year hourly average")  
    plt.plot(hour_prodction_mean, label = "Production")
    plt.plot(hour_consumption_mean, label = "Consumption") 
    plt.xlabel("hour")
    plt.ylabel("Energy in MWh")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    update_ar_model()
    


