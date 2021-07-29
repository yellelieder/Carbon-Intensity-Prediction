import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
import time
import numpy as np
import logging

RAW_PRODUCTION_FILE = r"Ressources\RawDataMerged\raw_production.csv"
RAW_CONSUMPTION_FILE = r"Ressources\RawDataMerged\raw_consumption.csv"
TARGET_PRODUCTION_FOLDER="Ressources\\Training Data Production\\"
TARGET_CONSUMPTION_FOLDER="Ressources\\Training Data Consumption\\"
TIME_STAMP = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("preprocessor.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)


def clean(type:str):
    '''
    Cleans data in scraped and merged csv files for auto regression.

        Parameters:
        ----------
        type : str
            The type of data. 1=production, 2=consumption
    '''
    file_index=1 if type=="1" else 0
    file_name="Production" if type=="1" else "Consumption"
    df=pd.read_csv("Ressources\\RawDataMerged\\"+sorted(os.listdir("Ressources\\RawDataMerged\\"))[file_index], sep=",", index_col=0)
    df=df.replace("-",0)
    df["Datum"]= df[['Datum', 'Uhrzeit']].agg(' '.join, axis=1)
    df["Datum"]=df["Datum"].apply(lambda x: re.sub("[.]","/", x)+":00")
    pd.DataFrame(clean_rows(type, df)).to_csv("Ressources\\TrainingData\\"+file_name+".csv")
    log.info(f"input: {type}, used to save cleaned df as csv: {file_name}.csv")

def clean_rows(type, df):
    '''
    Pre-processes the rows of a dataframe.

        Parameters:
        ----------
        type : str
            The type of data. 1=production, 2=consumption

        df : pf.DataFrame
            Dataframe containing production or consumption data.

        Returns:
        ----------
        df : pd.DataFrame
            Containing data ready for auto regression.
    '''
    if type=="1":
        log.info(f"formatting production data rows")
        df["Biomasse[MWh]"]=df["Biomasse[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wasserkraft[MWh]"]=df["Wasserkraft[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wind Offshore[MWh]"]=df["Wind Offshore[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Wind Onshore[MWh]"]=df["Wind Onshore[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Photovoltaik[MWh]"]=df["Photovoltaik[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Sonstige Erneuerbare[MWh]"]=df["Sonstige Erneuerbare[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        
        df={"Date":df["Datum"], "Production":
            df["Biomasse[MWh]"]+
            df["Wasserkraft[MWh]"]+
            df["Wind Offshore[MWh]"]+
            df["Wind Onshore[MWh]"]+
            df["Photovoltaik[MWh]"]+
            df["Sonstige Erneuerbare[MWh]"]}
    else:
        log.info(f"formating consumption data rows")
        df["Gesamt (Netzlast)[MWh]"]=df["Gesamt (Netzlast)[MWh]"].apply(lambda x: str(x).replace(".","").replace(",",".")).apply(lambda y: int(float(str(y))))
        df={"Date":df["Datum"], "Consumption":df["Gesamt (Netzlast)[MWh]"]}
    return df