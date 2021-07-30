import pandas as pd
p=str(pd.read_csv("Ressources\TrainingData\Production.csv", index_col=0, parse_dates=[1],sep=",").iloc[-1,0]).replace("-","/")
c=str(pd.read_csv("Ressources\TrainingData\Consumption.csv", index_col=0, parse_dates=[1],sep=",").iloc[-1,0]).replace("-","/")
print(str(min(p,c)))