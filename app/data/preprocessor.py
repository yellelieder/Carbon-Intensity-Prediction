import pandas as pd
import regex as re
import os
import numpy as np
import logger as log

def clean_files(type:str):
    '''
    Cleans raw data for machine learning training.

        Parameters:
        ----------
        type : str
            The type of data. 1=production, 2=consumption

        Returns:
        ----------
             
            Stores cleaned data as .csv and dataframe .pkl
    '''
    file_index=1 if type=="1" else 0
    file_name="Production" if type=="1" else "Consumption"
    df=pd.read_csv("Ressources\\RawDataMerged\\"+sorted(os.listdir("Ressources\\RawDataMerged\\"))[file_index], sep=",", index_col=0, dtype=object)
    df=df.replace("-",0)
    df["Datum"]= df[['Datum', 'Uhrzeit']].agg(' '.join, axis=1)
    df["Datum"]=df["Datum"].apply(lambda x: re.sub("[.]","/", x)+":00")
    pd.DataFrame(merge_columns(type, df)).to_csv("Ressources\\TrainingData\\"+file_name+".csv")
    df.to_pickle("Ressources\\TrainingData\\"+file_name+".pkl")
    log.add.info(f"input: {type}, used to save cleaned df as csv: {file_name}.csv")

def merge_columns(type, df):
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
        log.add.info(f"formatting production data rows")

        col = ["Biomasse[MWh]","Wasserkraft[MWh]","Wind Offshore[MWh]","Wind Onshore[MWh]","Photovoltaik[MWh]","Sonstige Erneuerbare[MWh]"]
        for c in col:
            df[c]=(df[c].apply(lambda x: str(x).replace(".",""))).apply(lambda x: str(x).replace(",",".")).apply(lambda y: int(float(str(y))))
            df[c==0]=np.nan
            mean=df[c].mean(skipna=True)
            df=df.replace({c: {0: mean}})
        df={"Date":df["Datum"], "Production":
            (df["Biomasse[MWh]"]+
            df["Wasserkraft[MWh]"]+
            df["Wind Offshore[MWh]"]+
            df["Wind Onshore[MWh]"]+
            df["Photovoltaik[MWh]"]+
            df["Sonstige Erneuerbare[MWh]"])}
        df["Production"]=(df["Production"].apply(lambda y: int(float(str(y)))))
    else:
        log.add.info(f"formating consumption data rows")
        df["Gesamt (Netzlast)[MWh]"]=(df["Gesamt (Netzlast)[MWh]"].apply(lambda x: str(x).replace(".",""))).apply(lambda x: str(x).replace(",",".")).apply(lambda y: int(float(str(y))))
        df["Gesamt (Netzlast)[MWh]"==0]=np.nan
        mean=df["Gesamt (Netzlast)[MWh]"].mean(skipna=True)
        df=df.replace({"Gesamt (Netzlast)[MWh]": {0: mean}})
        df={"Date":df["Datum"], "Consumption":df["Gesamt (Netzlast)[MWh]"]}
        df["Consumption"]=(df["Consumption"].apply(lambda y: int(float(str(y)))))    
    return df