import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
import time
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
    for row in df.index:
        date=df["Datum"][row]
        print("Date: ",date)
        #date=re.sub("[.]","/", str(df["Datum"][row]))+" "+df["Uhrzeit"][row]+":00"
        if type=="1":
            dict={"Date":date, "Renevables":
            int(float((str(df["Biomasse[MWh]"][row]).replace(".","")).replace(",",".")))+
            int(float((str(df["Wasserkraft[MWh]"][row]).replace(".","")).replace(",",".")))+
            int(float((str(df["Wind Offshore[MWh]"][row]).replace(".","")).replace(",",".")))+
            int(float((str(df["Wind Onshore[MWh]"][row]).replace(".","")).replace(",",".")))+
            int(float((str(df["Photovoltaik[MWh]"][row]).replace(".","")).replace(",",".")))+
            int(float((str(df["Sonstige Erneuerbare[MWh]"][row]).replace(".","")).replace(",",".")))}
        else:
            dict={"Date":date, "Consumption":int(str(df["Gesamt (Netzlast)[MWh]"][row]).replace(".",""))}
        clean_data= clean_data.append(dict, ignore_index=True)
    clean_data.to_csv("Ressources\\TrainingData\\"+file+"_"+timeStamp+".csv")
