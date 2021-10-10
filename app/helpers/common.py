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

def datetime_to_str(datetime_object):
    '''
    Converts datetime object to string dd/mm/yyyy hh:mm:ss

        Parameters:
        ----------

            datetime_object : datetime

        Returns:
        ----------

            date_time : str
    '''
    date_time=datetime.strftime(datetime_object, config.dateformat)
    log.add.info(f"converted datetime ({str(datetime_object)}) object to string ({date_time})")
    return date_time

def str_to_datetime(str_object):
    '''
    Converts Datetime str to datetime object.

        Parameters:
        ----------

            str_object : str

        Returns:
        ----------

            date_time : datetime
    '''
    date_time=datetime.strptime(str_object, config.dateformat)
    log.add.info(f"converted string ({str_object}) to datetime object ({date_time})")
    return date_time

def lag_to_datetime(period, start):
    '''
    Turns row index from training data into human readable time.

        Parameters:
        ----------

            period : int
                n-th row in training set, if one woult continue conting. 

        Returns:
        ----------

            date_time : str
                Exact time, accurate to 15 minutes.
    '''
    date_time=(str_to_datetime(start)+timedelta(seconds=period*900)).strftime(config.dateformat)
    log.add.info(f"converted {period}. lag of training data into datetime object ({date_time})")
    return date_time

def datetime_str_to_lag(time,type):
    '''
    Converts datetime object into row index of csv file.

        Parameters:
        ----------

            time : datetime

            type : str
                1 = Production, 2 = Consumption

        Returns:
        ----------

            lag : int
    '''
    input_time_index=datetime.strptime(time, config.dateformat)
    base_time_index = last_training_date(type=type)
    lag=int(divmod((input_time_index-base_time_index).total_seconds(),900)[0])-1
    log.add.info(f"converted datetime as string ({str(time)}) into {lag}. lag timeframe")
    return lag

def last_training_date(type:str) -> str:
    '''
    Returns last date where training data is available.

        Parameters:
        ----------

            type : str
                1 = Production, 2 = Consumption

        Returns:
        ----------

            date : str
    '''
    path = f"{config.training_data_folder}{type.capitalize()}.pkl"
    try:
        df=pd.read_pickle(path)
    except FileNotFoundError as exception:
        print_fnf(path, exception)
    date = df.iloc[-1,0]
    log.add.info(f"returnes last available date ({date}) for training date type {type}")
    return date

def format_date(date):
    '''
    Re-formats date as string.

        Parameters:
        ----------

            date : str
                Format: y-m-d h:m:s

        Returns:
        ----------

            date : str
                Format: d/m/y h:m:s
    '''
    date_time = datetime.strftime((datetime.strptime(str(date),"%Y-%m-%d %H:%M:%S")), config.dateformat)
    log.add.info(f"reformated {date} into {date_time}")
    return date_time

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
    file_name=sorted(os.listdir(dir)).pop()
    log.add.info(f"returned name of newest file ({file_name}) from {dir}")
    return file_name

def merge_date_and_time(date, time):
    '''
    Converts data and time to timestamp.

        Parameters:
        ----------

            date : str        
            time : str

        Returns:
        ----------

            date_time : str
                In form dd/mm/yyy hh:mm:ss
    '''
    date_time=str(re.sub("[.]","/", date)+" "+time+":00")
    log.add.info(f"merged {date} and {time} to {date_time}")
    return date_time

def print_fnf(file_details, exception):
    '''
    Handles FileNotFoundExceptions.

        Parameters:
        ----------

            file_details : str

            exception : FileNotFoundException

        Returns:
        ----------

            None : prints and loggs errors.
    '''
    print(f"ERROR: {file_details} file could not be found!\n Please restore original file form git and try again.")
    log.add.info(f"file ({file_details})) not found exception: {str(exception)}")
