from posix import listdir
import pandas as pd
from datetime import datetime
import regex as re
import matplotlib.pyplot as plt
import os
CONSUMPTION_FOLDER_PATH="Ressources\\Training Data Consumption\\"
PRODUCTION_FOLDER_PATH="Ressources\\Training Data Production\\"

def listDir(dir):
    fileNames=os.listdir(dir)
    fileNames=fileNames.sort()
    return fileNames[-1]

if __name__ == "__main__":
    listDir(CONSUMPTION_FOLDER_PATH)
    listDir(PRODUCTION_FOLDER_PATH)

df=pd.read_csv(CONSUMPTION_FOLDER_PATH+listdir(CONSUMPTION_FOLDER_PATH), sep=",")