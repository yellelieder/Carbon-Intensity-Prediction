import pandas as pd
import regex as re
import os
import numpy as np
import logger as log
import config

def clean_file(type:str):
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
    #order of files in folder
    file_index=1 if type=="1" else 0
    file_name="Production" if type=="1" else "Consumption"
    #reading raw data
    df=pd.read_csv(config.merged_data_folder+sorted(os.listdir(config.merged_data_folder))[file_index], sep=",", index_col=0, dtype=object)
    df=df.replace("-",0)
    #formatting datetime
    df["Datum"]= df[['Datum', 'Uhrzeit']].agg(' '.join, axis=1)
    df["Datum"]=df["Datum"].apply(lambda x: re.sub("[.]","/", x)+":00")
    #merging columns and storing result
    df=pd.DataFrame(_process_cols(type, df))
    #persisting as csv and pkl
    df.to_csv(config.training_data_folder+file_name+".csv")
    df.to_pickle(config.training_data_folder+file_name+".pkl")
    log.add.info(f"cleaned date persisted as {file_name}.csv/.pkl")

def _process_cols(type, df):
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
        columns = ["Biomasse[MWh]","Wasserkraft[MWh]","Wind Offshore[MWh]","Wind Onshore[MWh]","Photovoltaik[MWh]","Sonstige Erneuerbare[MWh]"]
        for column in columns:
            df[column]=(df[column].apply(lambda x: str(x).replace(".",""))).apply(lambda x: str(x).replace(",",".")).apply(lambda y: int(float(str(y))))
            df[column==0]=np.nan
            mean=df[column].mean(skipna=True)
            df=df.replace({column: {0: mean}})
        df={"Date":df["Datum"], "Production":
            (df["Biomasse[MWh]"]+
            df["Wasserkraft[MWh]"]+
            df["Wind Offshore[MWh]"]+
            df["Wind Onshore[MWh]"]+
            df["Photovoltaik[MWh]"]+
            df["Sonstige Erneuerbare[MWh]"])}
        df["Production"]=(df["Production"].apply(lambda y: int(float(str(y)))))
        log.add.info(f"Production data merged")
    else:
        mwh="Gesamt (Netzlast)[MWh]"
        df[mwh]=(df[mwh].apply(lambda x: str(x).replace(".",""))).apply(lambda x: str(x).replace(",",".")).apply(lambda y: int(float(str(y))))
        df[mwh==0]=np.nan
        mean=df[mwh].mean(skipna=True)
        df=df.replace({mwh: {0: mean}})
        df={"Date":df["Datum"], "Consumption":df[mwh]}
        df["Consumption"]=(df["Consumption"].apply(lambda y: int(float(str(y)))))    
        log.add.info(f"Consumption data merged")
    return df