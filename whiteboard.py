import pandas as pd

path = f"Ressources\TrainingData\Production.csv"
df=pd.read_csv(path, index_col=0, parse_dates=[1], sep=",")
df.to_pickle("Ressources\TrainingData\Production.pkl")
df=pd.read_pickle("Ressources\TrainingData\Production.pkl")
df.iloc[-1,0]
type="hello, WORLD"
print(type.capitalize())


path = f"Ressources\TrainingData\Consumption.csv"
df=pd.read_csv(path, index_col=0, parse_dates=[1], sep=",")
df.to_pickle("Ressources\TrainingData\Consumption.pkl")
df=pd.read_pickle("Ressources\TrainingData\Consumption.pkl")
df.iloc[-1,0]
type="hello, WORLD"
print(type.capitalize())