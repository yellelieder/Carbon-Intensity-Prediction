import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
CONSUMPTION_FOLDER_PATH="Ressources\\Training Data Consumption\\"
PRODUCTION_FOLDER_PATH="Ressources\\Training Data Production\\"

def getLatestFile(dir):
    return sorted(os.listdir(dir)).pop()

def parser(s):
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

if __name__ == "__main__":
    df_production=pd.read_csv(PRODUCTION_FOLDER_PATH+getLatestFile(PRODUCTION_FOLDER_PATH), index_col=0, parse_dates=[1],sep=",")
    plt.plot(df_production["Date"],df_production["Renevables"])
    plt.ylabel("Production")
    plt.xlabel("Time")
    plt.show()
    print(df_production)
    df_consumption=pd.read_csv(CONSUMPTION_FOLDER_PATH+getLatestFile(CONSUMPTION_FOLDER_PATH), index_col=0, parse_dates=[1],sep=",")
    plt.plot(df_consumption["Date"], df_consumption["Consumption"])
    plt.ylabel("Consumption")
    plt.show()
    print(df_consumption)