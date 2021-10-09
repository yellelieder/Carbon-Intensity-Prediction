from datetime import date, timedelta
from flask import Flask, request, jsonify,render_template, flash, redirect, make_response
from flask_restful import Resource, Api
from datetime import datetime
import regex as re
import requests
import json
from flask_apscheduler import APScheduler
import logging
import traceback
from flask_wtf import FlaskForm
from requests.models import requote_uri
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import markdown.extensions
import pandas as pd
import os

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

def log(x:str):
    log.info(x)

def datetime_to_str(s):
    return datetime.strftime(s, "%d/%m/%Y %H:%M:%S")

def str_to_datetime(s):
    return datetime.strptime(s, "%d/%m/%Y %H:%M:%S")

def time_str_to_lag(time,type):
    input_time_index=datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    base_time_index = last_training_date(type=type)
    #base_time_index=datetime.strptime("14/09/2021 23:45:00", '%d/%m/%Y %H:%M:%S')
    return int(divmod((input_time_index-base_time_index).total_seconds(),900)[0])

def lag_to_datetime(period, start):
    '''
        Turns row index from training data into human readable time.

        Parameters:
        ----------
        period : int
            n-th row in training set, if one woult continue conting. 

        Returns:
        ----------
        date_time : datetime
            Exact time, accurate to 15 minutes.
    '''
    return (str_to_datetime(start)+timedelta(seconds=period*900)).strftime('%d/%m/%Y %H:%M:%S')

def datetime_str_to_lag(time,type):
    input_time_index=datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    base_time_index = last_training_date(type=type)
    return int(divmod((input_time_index-base_time_index).total_seconds(),900)[0])-1

def last_training_date(type:str):
    path = f"Ressources\TrainingData\{type.capitalize()}.pkl"
    df=pd.read_pickle(path)
    return df.iloc[-1,0]

def format_date(date):
    return datetime.strftime((datetime.strptime(str(date),"%Y-%m-%d %H:%M:%S")), "%d/%m/%Y %H:%M:%S")

def get_latest_file(dir):
    '''
    Returns last file form folder by alphabetical order.

        Parameters:
        ----------

        dir : str
            Folder to search from.

        Returns:
        ----------

        file_name : str
            Name of the last file from the folder in alphabetical order.
    '''
    return sorted(os.listdir(dir)).pop()