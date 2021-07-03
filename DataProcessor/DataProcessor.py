import csv
import pandas as pd
from datetime import datetime
import regex as re
rawProduction = "Ressources\\rawDataProduction.csv"
rawConsumption = "Ressources\\rawDataConsumption.csv"

timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

df=pd.DataFrame(pd.read_csv(rawProduction))


df.to_csv("Ressources\\Training Data Production\\trainingProduction_"+timeStamp+".csv")

print(df.loc[1]+df.loc[2])
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