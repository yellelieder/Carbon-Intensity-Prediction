import pandas as pd
#where I try out stuff


p=pd.read_csv("Ressources\TrainingData\Production.csv", index_col=0, parse_dates=[1],sep=",")
c=pd.read_csv("Ressources\TrainingData\Consumption.csv", index_col=0, parse_dates=[1],sep=",")
timestampA= pd.to_datetime(p.iloc[-1,0]).strftime("%d-%m-%Y %H:%M:%S")
timestampB= pd.to_datetime(c.iloc[-1,0]).strftime("%d-%m-%Y %H:%M:%S")
print(str(min(timestampA,timestampB)).replace("-","/"))




