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
import config
import logger as log

def datetime_to_str(s):
    return datetime.strftime(s, config.dateformat)

def str_to_datetime(s):
    return datetime.strptime(s, config.dateformat)

def time_str_to_lag(time,type):
    input_time_index=datetime.strptime(time, config.dateformat)
    base_time_index = last_training_date(type=type)
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

def merge_data_and_time(date, time):
    '''
    Converts data and time to timestamp.

        Parameters:
        ----------

        date : str        
        time : str
            User input when process can start.

        Returns:
        ----------

        date_time : str
            In form dd/mm/yyy hh:mm:ss
    '''
    return str(re.sub("[.]","/", date)+" "+time+":00")