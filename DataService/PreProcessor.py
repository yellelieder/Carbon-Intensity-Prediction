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

def clean_date(date):
    return re.sub("[.]","/", date)+":00"

def clean(type:str):
    if type=="1":
        file_index=1
        file="Production"
        clean_data=pd.DataFrame(columns=["Date","Renevables"])
    else:
        file_index=0
        file="Consumption"
        clean_data=pd.DataFrame(columns=["Date","Consumption"])
    df=pd.read_csv("Ressources\\RawDataMerged\\"+sorted(os.listdir("Ressources\\RawDataMerged\\"))[file_index], sep=",", index_col=0)

    df=df.replace("-",0)
    df["Datum"]= df[['Datum', 'Uhrzeit']].agg(' '.join, axis=1)
    df["Datum"]=df["Datum"].apply(lambda x: re.sub("[.]","/", x)+":00")
    if type=="1":
        df["Biomasse[MWh]"]=df["Biomasse[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wasserkraft[MWh]"]=df["Wasserkraft[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wind Offshore[MWh]"]=df["Wind Offshore[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wind Onshore[MWh]"]=df["Wind Onshore[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Photovoltaik[MWh]"]=df["Photovoltaik[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Sonstige Erneuerbare[MWh]"]=df["Sonstige Erneuerbare[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        
        for row in df.index:
            dict={"Date":df["Datum"][row], "Renevables":
            int(float((str(df["Biomasse[MWh]"][row]))))+
            int(float((str(df["Wasserkraft[MWh]"][row]))))+
            int(float((str(df["Wind Offshore[MWh]"][row]))))+
            int(float((str(df["Wind Onshore[MWh]"][row]))))+
            int(float((str(df["Photovoltaik[MWh]"][row]))))+
            int(float((str(df["Sonstige Erneuerbare[MWh]"][row]))))}
            clean_data= clean_data.append(dict, ignore_index=True)
    else:
        df["Gesamt (Netzlast)[MWh]"]=df["Gesamt (Netzlast)[MWh]"].apply(lambda x: str(x).replace(".","").replace(",","."))
        for row in df.index:
            #if error: remove float casting
            dict={"Date":df["Datum"][row], "Consumption":int(float(str(df["Gesamt (Netzlast)[MWh]"][row])))}
            clean_data= clean_data.append(dict, ignore_index=True)
    clean_data.to_csv("Ressources\\TrainingData\\"+file+"_"+timeStamp+".csv")
