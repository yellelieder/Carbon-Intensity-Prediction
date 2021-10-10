from datetime import date, timedelta
from flask import Flask, request, jsonify,render_template, flash, redirect, make_response
from flask_restful import Resource, Api
from datetime import datetime
import regex as re
import requests
import json
from flask_apscheduler import APScheduler, scheduler
import logging
import traceback
from flask_wtf import FlaskForm
from requests.models import requote_uri
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import markdown
from app.helpers import inputvalidation
from app.prediction import predictionhandler
from app.helpers import common
import config
import logger as log

class EPI(Resource):
    def get(self):
        '''
        Handles users get request with prediction in form of json.

        Parameters:
        ----------

            self : object of type EPI
                basically the app

        Returns:
        ----------

            response : json
                response to the request
        '''
        log.add.info(f"handling get request in /api/ directory: {request}")
        query=request.args 
        result= prediction(query.get("lat", type=float),query.get("long", type=float),query.get("stdate"), query.get("sttime"), query.get("endate"),query.get("entime"),query.get("dur", type=int))
        log.add.info(f"send response for API call: {result}")
        return result

class TestEndpoint(Resource):
    def get(self):
        '''
        Handles request for testing purposes.
        Uses same mechanics under the hood, but skips validation and weather forcasts.

        Parameters:
        ----------
            self : object of type TestEndPoint  

        Returns:
        ----------

            response : json
                response to the request
        '''
        log.add.info(f"handling get request in /api/ directory: {request}")
        query=request.args 
        result= _test_prediction(query.get("lat", type=float),query.get("long", type=float),query.get("stdate"), query.get("sttime"), query.get("endate"),query.get("entime"),query.get("dur", type=int))
        log.add.info(f"send response for API TEST call: {result}")
        return result

class Home(Resource):
    def get(self):
        '''
        Shows home page to the user.

        Parameters:
        ----------

            self : object of type Home

        Returns:
        ----------

            result : html
        '''
        headers = {'Content-Type': 'text/html'}
        result= make_response(render_template(r'index.html'),200,headers)
        log.add.info(f"displayed index.html webapp screen")
        return result

class Usage_Docu(Resource):
    def get(self):
        '''
        Shows api deatils page to the user.

        Parameters:
        ----------

            self : object of type Home

        Returns:
        ----------

            result : html
        '''
        headers = {'Content-Type': 'text/html'}
        result=  make_response(render_template(r'api.html'),200,headers)
        log.add.info(f"displayed api.html explaination screen")
        return result

class Technical_Docu(Resource):
    def get(self):
        '''
        Shows technical documentation page to the user.

        Parameters:
        ----------

            self : object of type Home

        Returns:
        ----------

            result : html
        '''
        headers = {'Content-Type': 'text/html'}
        result= make_response(render_template(r'docu.html'),200,headers)
        log.add.info(f"displayed docu.html documentation")
        return result

class Imprint(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        result= make_response(render_template(r'imprint.html'),200,headers)
        log.add.info(f"displayed imprint.html screen")
        return result

class App(Resource):
    def get(self):
        '''
        Shows input form page to the user.

        Parameters:
        ----------

            self : object of type Home

        Returns:
        ----------

            result : html
        '''
        headers = {'Content-Type': 'text/html'}
        result= make_response(render_template(r'form.html'),200,headers)
        log.add.info(f"displayed form.html visual input App")
        return result

    def post(self):
        '''
        Converts user form inputs to prediction.

        Parameters:
        ----------

            self : object of type Home

        Returns:
        ----------

            result : html
        '''
        lat =float(request.form["lat"])
        lng =float(request.form["lng"])
        stdate=str(datetime.strptime(request.form["stdate"], '%Y-%m-%d').strftime("%d/%m/%Y"))
        sttime =str(request.form["sttime"])
        enddate=str(datetime.strptime(request.form["enddate"], '%Y-%m-%d').strftime("%d/%m/%Y"))
        endtime =str(request.form["endtime"])
        dur = int(request.form["dur"])
        pred=prediction(lat, lng, stdate, sttime, enddate, endtime, dur)[0]
        headers = {'Content-Type': 'text/html'}
        result= make_response(render_template(r'result.html', key=list(pred.keys())[0], value=list(pred.values())[0]),headers)
        log.add.info(f"received input from visual form")
        return result

def _test_prediction(lat, lng, stdate, sttime, enddate, endtime, dur)->json:
    '''
    Handles test prediction but skips input validation.

    Input validation must be skipped to be able to backtest.

    Parameters:
    ----------

        self : object of type Home

    Returns:
    ----------

        result : json
    '''
    start=common.merge_date_and_time(stdate,sttime)
    end=common.merge_date_and_time(enddate,endtime)
    result=predictionhandler.run(lat, lng, start, end, dur, "test")
    result = {"ideal start":result[0],"fits data":result[1], "randome success":result [2]}, 200
    log.add.info(f"returned test prediction")
    return result


def prediction(lat, lng, stdate, sttime, enddate, endtime, dur)->json:
    '''
    Performs input validation.

    Parameters:
    ----------

        self : object of type Home

    Returns:
    ----------

        result : json
    '''
    error_key_name="error"
    start=common.merge_date_and_time(stdate,sttime)
    end=common.merge_date_and_time(enddate,endtime)
    if dur<15:
        return {error_key_name:"duration must be minimum of 15 min"}, 406 
    elif inputvalidation.start_after_end(start, end):
        return {error_key_name:"end before start"}, 406 
    elif inputvalidation.start_in_past(start):
        return {error_key_name:"enter upcoming timeframe"}, 406  
    elif inputvalidation.time_le_dur(start, end, dur):
        return {error_key_name:"duration not fitting in timeframe"}, 406
    elif lat<-90 or lat>90:
        return {error_key_name:"lattitude out of rang"}, 406
    elif lng<-180 or lng>180:
        return {error_key_name:"longitude out of range"}, 406
    elif inputvalidation.invalid_geo(lat, lng):  
        return {error_key_name:"enter german coodrinates"}, 406  
    else:
        result = {"ideal start":predictionhandler.run(lat, lng, start, end, dur, test="no")}, 200
        log.add.info(f"all validations successfull, returned prediction")
        return result
