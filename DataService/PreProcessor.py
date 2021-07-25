import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
RAW_PRODUCTION_FILE = r"Ressources\RawDataMerged\raw_production.csv"
RAW_CONSUMPTION_FILE = r"Ressources\RawDataMerged\raw_consumption.csv"
TARGET_PRODUCTION_FOLDER="Ressources\\Training Data Production\\"
TARGET_CONSUMPTION_FOLDER="Ressources\\Training Data Consumption\\"
timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def b():
    

    df=pd.read_csv(RAW_PRODUCTION_FILE, sep=";")
    cleanProdData=pd.DataFrame(columns=["Date","Renevables"])
    #cleanConData=pd.DataFrame(columns=["Date","Consumption"])
    for row in df.iterrows():
        date=re.sub(".","/", row[0])+" "+row[1]+":00"
        dict={"Date":date, "Renevables":int(float((str(row[2]).replace(".","")).replace(",",".")))+int(float((str(row[3]).replace(".","")).replace(",",".")))+int(float((str(row[4]).replace(".","")).replace(",",".")))+int(float((str(row[5]).replace(".","")).replace(",",".")))+int(float((str(row[6]).replace(".","")).replace(",",".")))+int(float((str(row[7]).replace(".","")).replace(",",".")))}
        cleanProdData= cleanProdData.append(dict, ignore_index=True)
    cleanProdData.to_csv(TARGET_PRODUCTION_FOLDER+"trainingProduction_"+timeStamp+".csv")

def clean(type:str):
    if type=="1":
        pop=1
        file="Production"
        clean_data=pd.DataFrame(columns=["Date","Renevables"])
    else:
        pop=0
        file="Consumption"
        clean_data=pd.DataFrame(columns=["Date","Consumption"])
    df=pd.read_csv("Ressources\\RawDataMerged\\"+sorted(os.listdir("Ressources\\RawDataMerged\\"))[pop], sep=";", index_col=0)
    for row in df.iterrows():
        print("-----")
        print("Row: ", row)
        print("-----")
        date=re.sub(".","/", str(row[0]))+" "+str(row[1])+":00"
        print(date)
        if type=="1":
            dict={"Date":date, "Renevables":int(float((str(row[2]).replace(".","")).replace(",",".")))+int(float((str(row[3]).replace(".","")).replace(",",".")))+int(float((str(row[4]).replace(".","")).replace(",",".")))+int(float((str(row[5]).replace(".","")).replace(",",".")))+int(float((str(row[6]).replace(".","")).replace(",",".")))+int(float((str(row[7]).replace(".","")).replace(",",".")))}
        else:
            dict={"Date":date, "Consumption":int(str(row[2]).replace(".",""))}
        clean_data= clean_data.append(dict, ignore_index=True)
    clean_data.to_csv("Ressources\\TrainingData\\"+file+"_"+timeStamp+".csv")

if __name__=="__main__":
    clean("1")