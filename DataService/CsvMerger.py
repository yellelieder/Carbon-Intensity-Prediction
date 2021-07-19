import pandas as pd

TARGET_FOLDER="Ressources\\RawDataMerged\\RawDataMerged"

def merge(type:str, first_file, second_file):
    first_df=pd.read_csv(first_file, sep=";")
    second_df=pd.read_csv(second_file, sep=";")
    df=first_df.append(second_df, ignore_index=True)
    df.to_csv(TARGET_FOLDER+type.capitalize()+"\\"+"raw_"+type+"_"+str(df.iloc[0,0]).replace(".","_")+"_to_"+str(df.iloc[-1,0]).replace(".","_")+".csv")

if __name__=="__main__":
    merge("production","Ressources\\Downloads\\rawDateProduction2019.csv", "Ressources\\Downloads\\rawDateProduction2020.csv")