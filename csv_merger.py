import pandas as pd
from datetime import datetime
import regex as re
OLDER = "Ressources\\older.csv"
NEWER = "Ressources\\newer.csv"
TARGET_PRODUCTION_FOLDER="Ressources\\Training Data Production\\"

timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

older_file=pd.read_csv(OLDER, sep=";")
cleanOldData=pd.DataFrame(columns=["Date","Renevables"])
for i, row in older_file.iterrows():
    date=re.sub("[.]","/", row[0])+" "+row[1]+":00"
    dict={"Date":date, "Renevables":int(float((str(row[2]).replace(".","")).replace(",",".")))+int(float((str(row[3]).replace(".","")).replace(",",".")))+int(float((str(row[4]).replace(".","")).replace(",",".")))+int(float((str(row[5]).replace(".","")).replace(",",".")))+int(float((str(row[6]).replace(".","")).replace(",",".")))+int(float((str(row[7]).replace(".","")).replace(",",".")))}
    print(dict)
    cleanOldData= cleanOldData.append(dict, ignore_index=True)

newer_file=pd.read_csv(NEWER, sep=";")
cleanNewData=pd.DataFrame(columns=["Date","Renevables"])
for i, row in newer_file.iterrows():
    date=re.sub("[.]","/", row[0])+" "+row[1]+":00"
    dict={"Date":date, "Renevables":int(str(row[2]).replace(".",""))+int(str(row[3]).replace(".",""))+int(str(row[4]).replace(".",""))+int(str(row[5]).replace(".",""))+int(str(row[6]).replace(".",""))+int(str(row[7]).replace(".",""))}
    print(dict)
    cleanNewData= cleanNewData.append(dict, ignore_index=True)

cleanOldData.append(cleanNewData, ignore_index=True)
cleanOldData.to_csv(TARGET_PRODUCTION_FOLDER+"merged_production_"+timeStamp+".csv")

