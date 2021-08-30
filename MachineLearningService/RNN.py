import numpy as np
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import matplotlib.pyplot as plt
import regex as re
from datetime import datetime
import os
import logging
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


CONSUMPTION_DATA_FOLDER_PATH="Ressources\\Training Data Consumption\\"
CONSUMPTION_MODEL_FOLDER_PATH ="Ressources\\Models Consumption\\"
NO_OF_DAYS_TO_PREDICT=7

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
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
    predition_lenght = NO_OF_DAYS_TO_PREDICT*96
    train=df[:len(df)-predition_lenght]
    test=df[len(df)-predition_lenght:]
    scaler = MinMaxScaler
    scaled_train = scaler.transform(train)
    scaled_test = scaler.transform(test)  
    n_input=96*6
    n_features =1
    generator = TimeseriesGenerator(scaled_train, scaled_test, length=n_input, batch_size=1)
    model = Sequential()
    model.add(LSTM(100, activation="relu", input_shape=(n_input, n_features)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    model.summary()
    model.fit(generator, epochs=50)
    loss_per_epoch=model.history.history["loss"]
    plt.plot(range(len(loss_per_epoch)), loss_per_epoch)





if __name__ == "__main__":
    updateModel("production")