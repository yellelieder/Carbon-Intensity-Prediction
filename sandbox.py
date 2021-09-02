from datetime import datetime
import pandas as pd
import os
from matplotlib import pyplot as plt
'''dir="Ressources\Downloads\Production"
data=pd.DataFrame()
for i in os.listdir(dir):
    file=pd.read_csv(dir+"\\"+i, sep=";", dtype=object)
    data=data.append(file, ignore_index=True)
df = pd.DataFrame(data)

df.plot(x="Date",y="Productioin")

#todo: handle existence of multiple files in folder
df.to_csv("Ressources\Experimental\\"+dir.split("\\")[2]+".csv")'''
file=pd.read_csv("Ressources\TrainingData\Consumption.csv", sep=",", index_col=0, parse_dates=[1], dtype={"Consumption": int})
file.plot(x="Date", y="Consumption")
plt.show()
