from datetime import date, timedelta
from flask import Flask, request, jsonify,render_template, flash, redirect, make_response
from flask_restful import Resource, Api
from app.prediction import predictionhandler
from datetime import datetime
import regex as re
import requests
import json
from flask_apscheduler import APScheduler
import logging
import traceback
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import markdown.extensions.fenced_code
import config
import logger as log

def start_after_end(start, end):
    '''
    Checks if start and end time are compatible.

        Parameters:
        ----------
        start : str
            Ealiest time process can be started.
        
        end : str
            Latest time process must be finished.            

        Returns:
        ----------

        valitation : bool
            False if input is valid, True if input is invalid.
    '''
    log.add.info(f"validating user input start and end time")
    return datetime.strptime(start, config.dateformat)>datetime.strptime(end, config.dateformat)

def start_in_past(start):
    '''
    Checks if user input is already in the past. 

        Parameters:
        ----------
        start : str
            Date to be validated. 

        Returns:
        ----------
        validation : bool
            False if input is valid, True if input is in the past.
    '''
    log.add.info(f"validating user input start")
    return datetime.strptime(start, config.dateformat)<datetime.now()

def time_le_dur(start, end, dur):
    '''
    Checks if duration fits into given timeframe.

        Parameters:
        ----------
        start : str
            Where duration can start.
        
        end : str
            Where duration must end.

        dur : int
            Duration in minutes.

        Returns:
        ----------
        validation : bool
            False if input is valid, true if duration does not fit between start and end.
    '''
    log.add.info(f"validating user input start, end, duration")
    return not int(divmod((datetime.strptime(end, config.dateformat)-datetime.strptime(start, config.dateformat)).total_seconds(),900)[0])>=int(dur/15)

def invalid_geo(lat, lng):
    '''
    Checks weather geo coordinates are in germany.

        Parameters:
        ----------
        lat : str
            Geographical lattitude.
        
        lng : str 
            Geographical longitude.

        Returns:
        ----------
        validation : bool
            False if coordinates are in Germany, true if they are outside germany.
    '''
    log.add.info(f"validation user geo coordinates")
    try:
        response=requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&result_type=country&key={config.googlemaps_api_key}").json()["results"][0]["formatted_address"]
    except Exception as e:
        return True
    if response=="Germany":
        return False
    else:
        return True