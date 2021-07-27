import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
import time
import numpy as np
RAW_PRODUCTION_FILE = r"Ressources\RawDataMerged\raw_production.csv"
RAW_CONSUMPTION_FILE = r"Ressources\RawDataMerged\raw_consumption.csv"
TARGET_PRODUCTION_FOLDER="Ressources\\Training Data Production\\"
TARGET_CONSUMPTION_FOLDER="Ressources\\Training Data Consumption\\"
timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def clean(type:str):
    """formats dataframe for ml training and saves it as csv"""
    if type=="1":
        file_index=1
        file="Production"
    else:
        file_index=0
        file="Consumption"
    df=pd.read_csv("Ressources\\RawDataMerged\\"+sorted(os.listdir("Ressources\\RawDataMerged\\"))[file_index], sep=",", index_col=0)
    df=df.replace("-",0)
    df["Datum"]= df[['Datum', 'Uhrzeit']].agg(' '.join, axis=1)
    df["Datum"]=df["Datum"].apply(lambda x: re.sub("[.]","/", x)+":00")
    pd.DataFrame(clean_rows(type, df)).to_csv("Ressources\\TrainingData\\"+file+".csv")

def clean_rows(type, df):
    """formats row according to the file type (production/consumption)"""
    if type=="1":
        df["Biomasse[MWh]"]=df["Biomasse[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wasserkraft[MWh]"]=df["Wasserkraft[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wind Offshore[MWh]"]=df["Wind Offshore[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wind Onshore[MWh]"]=df["Wind Onshore[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Photovoltaik[MWh]"]=df["Photovoltaik[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Sonstige Erneuerbare[MWh]"]=df["Sonstige Erneuerbare[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        
        df={"Date":df["Datum"], "Renevables":
            df["Biomasse[MWh]"]+
            df["Wasserkraft[MWh]"]+
            df["Wind Offshore[MWh]"]+
            df["Wind Onshore[MWh]"]+
            df["Photovoltaik[MWh]"]+
            df["Sonstige Erneuerbare[MWh]"]}
    else:
        df["Gesamt (Netzlast)[MWh]"]=df["Gesamt (Netzlast)[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df={"Date":df["Datum"], "Consumption":df["Gesamt (Netzlast)[MWh]"]}
    return df