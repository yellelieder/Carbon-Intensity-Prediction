import numpy as np
import torch 
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import matplotlib.pyplot as plt
import regex as re
from datetime import datetime
import os
import logging

CONSUMPTION_DATA_FOLDER_PATH="Ressources\\Training Data Consumption\\"
CONSUMPTION_MODEL_FOLDER_PATH ="Ressources\\Models Consumption\\"

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("autoregression.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)


timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def getLatestFile(dir):
    return sorted(os.listdir(dir)).pop()

def parser(s):
    return datetime.strftime(s,"%d/%m/%Y %H:%M:%S")

def updateModel(type):
    log.info(f"updating the rnn model of type: {type}")
    df=pd.read_csv(f"Ressources\\Training Data {type}\\"+getLatestFile(f"Ressources\\Training Data {type}\\"), index_col=0, parse_dates=[1],sep=",")
    df.head()



if __name__ == "__main__":
    updateModel("production")