import pandas as pd
from datetime import datetime
import regex as re
rawProduction = "Ressources\\rawDataProduction.csv"
rawConsumption = "Ressources\\rawDataConsumption.csv"
productionTargetFolder="Ressources\\Training Data Production\\"
consumptionTargetFolder="Ressources\\Training Data Consumption\\"

timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

df=pd.read_csv(rawProduction, sep=";")
d={"Date":"n","Renevables":"n"}
cleanData=pd.DataFrame(columns=["Date","Renevables"])
for i, row in df.iterrows():
    date=re.sub("[.]","/", row[0])+" "+row[1]+":00"
    dict={"Date":date, "Renevables":row[2]+row[3]+row[4]+row[5]+row[6]+row[7]}
    cleanData= cleanData.append(dict, ignore_index=True)
    print(cleanData)
cleanData.to_csv(productionTargetFolder+"trainingProduction_"+timeStamp+".csv")

# "Datum"
# "Uhrzeit";

# "Biomasse[MWh]";
# "Wasserkraft[MWh]";
# "Wind Offshore[MWh]";
# "Wind Onshore[MWh]";
# "Photovoltaik[MWh]";
# "Sonstige Erneuerbare[MWh]";

# "Kernenergie[MWh]";
# "Braunkohle[MWh]";
# "Steinkohle[MWh]";
# "Erdgas[MWh]";
# "Pumpspeicher[MWh]";
# "Sonstige Konventionelle[MWh]"



#Datum;
# Uhrzeit;
# Gesamt (Netzlast)[MWh];
# Residuallast[MWh];
# Pumpspeicher[MWh]