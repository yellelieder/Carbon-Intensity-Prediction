import pandas as pd
import regex as re
import os
import numpy as np
import logger as log
import config
from app.helpers import common

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
    file_index=1 if type==config.p_id else 0
    file_name=config.p if type==config.p_id else config.c
    #reading raw data
    file=config.merged_data_folder+sorted(os.listdir(config.merged_data_folder))[file_index]
    try:
        df=pd.read_csv(file, sep=",", index_col=0, dtype=object)
    except FileNotFoundError:
        common.print_fnf(file)
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
    if type==config.p_id:
        columns = ["Biomasse[MWh]","Wasserkraft[MWh]","Wind Offshore[MWh]","Wind Onshore[MWh]","Photovoltaik[MWh]","Sonstige Erneuerbare[MWh]"]
        for column in columns:
            df[column]=(df[column].apply(lambda x: str(x).replace(".",""))).apply(lambda x: str(x).replace(",",".")).apply(lambda y: int(float(str(y))))
            df[column==0]=np.nan
            mean=df[column].mean(skipna=True)
            df=df.replace({column: {0: mean}})
        df={"Date":df["Datum"], config.p:
            (df[columns[0]]+
            df[columns[1]]+
            df[columns[2]]+
            df[columns[3]]+
            df[columns[4]]+
            df[columns[5]])}
        df[config.p]=(df[config.p].apply(lambda y: int(float(str(y)))))
        log.add.info(f"Production data merged")
    else:
        mwh="Gesamt (Netzlast)[MWh]"
        df[mwh]=(df[mwh].apply(lambda x: str(x).replace(".",""))).apply(lambda x: str(x).replace(",",".")).apply(lambda y: int(float(str(y))))
        df[mwh==0]=np.nan
        mean=df[mwh].mean(skipna=True)
        df=df.replace({mwh: {0: mean}})
        df={"Date":df["Datum"], config.c:df[mwh]}
        df[config.c]=(df[config.c].apply(lambda y: int(float(str(y)))))    
        log.add.info(f"Consumption data merged")
    return df