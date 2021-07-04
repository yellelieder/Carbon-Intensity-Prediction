import pandas as pd
from datetime import datetime
import regex as re
rawProduction = "Ressources\\rawDataProduction.csv"
rawConsumption = "Ressources\\rawDataConsumption.csv"
productionTargetFolder="Ressources\\Training Data Production\\"
consumptionTargetFolder="Ressources\\Training Data Consumption\\"

timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def convertProduction():
    df=pd.read_csv(rawProduction, sep=";")
    cleanProdData=pd.DataFrame(columns=["Date","Renevables"])
    for i, row in df.iterrows():
        date=re.sub("[.]","/", row[0])+" "+row[1]+":00"
        dict={"Date":date, "Renevables":int(str(row[2]).replace(".",""))+int(str(row[3]).replace(".",""))+int(str(row[4]).replace(".",""))+int(str(row[5]).replace(".",""))+int(str(row[6]).replace(".",""))+int(str(row[7]).replace(".",""))}
        cleanProdData= cleanProdData.append(dict, ignore_index=True)
    cleanProdData.to_csv(productionTargetFolder+"trainingProduction_"+timeStamp+".csv")

def convertConsumption():
    df=pd.read_csv(rawConsumption, sep=";")
    cleanConData=pd.DataFrame(columns=["Date","Consumption"])
    for i, row in df.iterrows():
        date=re.sub("[.]","/", row[0])+" "+row[1]+":00"
        dict={"Date":date, "Consumption":int(str(row[2]).replace(".",""))}
        cleanConData= cleanConData.append(dict, ignore_index=True)
    cleanConData.to_csv(consumptionTargetFolder+"trainingConsumption_"+timeStamp+".csv")
