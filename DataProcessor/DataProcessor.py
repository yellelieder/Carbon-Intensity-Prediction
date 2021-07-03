import csv
import pandas as pd
from datetime import datetime
import regex as re
rawProduction = "Ressources\\rawDataProduction.csv"
rawConsumption = "Ressources\\rawDataConsumption.csv"
productionTargetFolder="Ressources\\Training Data Production\\"
consumptionTargetFolder="Ressources\\Training Data Consumption\\"

timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

df=pd.read_csv(rawProduction)
print(df.head())
print(df.loc[3])
#df.to_csv(productionTargetFolder+"trainingProduction_"+timeStamp+".csv")

#"Datum"
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