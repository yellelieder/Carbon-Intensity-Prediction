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
import ValidationHelper
from Prediction import PredictionHandler
# from DataService import Scraper, PreProcessor
# from MachineLearningService import Trainer

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

APP=Flask(__name__)
API=Api(APP)
SCHEDULER=APScheduler()

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
        log.info(f"handling get request in /api/ directory: {request}")
        query=request.args 
        return get_prediction(query.get("lat", type=float),query.get("long", type=float),query.get("stdate"), query.get("sttime"), query.get("endate"),query.get("entime"),query.get("dur", type=int))

class TestEndpoint(Resource):
    def get(self):
        log.info(f"handling get request in /api/ directory: {request}")
        query=request.args 
        return test_prediction(query.get("lat", type=float),query.get("long", type=float),query.get("stdate"), query.get("sttime"), query.get("endate"),query.get("entime"),query.get("dur", type=int))

def test_prediction(lat, lng, stdate, sttime, enddate, endtime, dur):
    start=to_timestamp(stdate,sttime)
    end=to_timestamp(enddate,endtime)
    result=PredictionHandler.run(lat, lng, start, end, dur, "test")
    return {"ideal start":result[0],"fits data":result[1], "randome success":result [2]}, 200


def get_prediction(lat, lng, stdate, sttime, enddate, endtime, dur):
    try:
        start=to_timestamp(stdate,sttime)
        end=to_timestamp(enddate,endtime)
        if dur<15:
            return {"error":"duration must be minimum of 15 min"}, 406 
        elif ValidationHelper.start_after_end(start, end):
            return {"error":"end before start"}, 406 
        elif ValidationHelper.start_in_past(start):
            return {"error":"enter upcoming timeframe"}, 406  
        elif ValidationHelper.time_le_dur(start, end, dur):
            return {"error":"duration not fitting in timeframe"}, 406
        elif lat<-90 or lat>90:
            return {"error":"lattitude out of rang"}, 406
        elif lng<-180 or lng>180:
            return {"error":"longitude out of range"}, 406
        elif ValidationHelper.invalid_geo(lat, lng):  
            return {"error":"enter german coodrinates"}, 406  
        else:
            log.info(f"input valid")
            return {"ideal start":PredictionHandler.run(lat, lng, start, end, dur, test="no")}, 200
    except Exception as e:
        log.info(f"error: {str(e)}")
        traceback.print_exc(e)
        return {"error":"invalid input"}, 406

class Home(Resource):
    def get(self):
        '''
        Shows forms for inputs to user.

        Parameters:
        ----------

        self : object of type home

        Returns:
        ----------

        GUI
        '''
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('base.html'),200,headers)

class Usage_Docu(Resource):
    def get(self):
        '''
        Shows forms for inputs to user.

        Parameters:
        ----------

        self : object of type home

        Returns:
        ----------

        GUI
        '''
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('api-docu.html'),200,headers)

class Technical_Docu(Resource):
    def get(self):
        '''
        Shows forms for inputs to user.

        Parameters:
        ----------

        self : object of type home

        Returns:
        ----------

        GUI
        '''
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('api-design-docu.html'),200,headers)

class Imprint(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('imprint.html'),200,headers)

class App(Resource):
    def get(self):
        '''
        Shows forms for inputs to user.

        Parameters:
        ----------

        self : object of type home

        Returns:
        ----------

        GUI
        '''
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('visual-app.html'),200,headers)

    def post(self):
        lat =float(request.form["lat"])
        lng =float(request.form["lng"])
        stdate=str(datetime.strptime(request.form["stdate"], '%Y-%m-%d').strftime("%d/%m/%Y"))
        sttime =str(request.form["sttime"])
        enddate=str(datetime.strptime(request.form["enddate"], '%Y-%m-%d').strftime("%d/%m/%Y"))
        endtime =str(request.form["endtime"])
        dur = int(request.form["dur"])
        pred=get_prediction(lat, lng, stdate, sttime, enddate, endtime, dur)[0]
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('result.html', key=list(pred.keys())[0], value=list(pred.values())[0]),headers)


def to_timestamp(date, time):
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

API.add_resource(EPI,"/api/")
API.add_resource(TestEndpoint,"/test/")
API.add_resource(Home,"/")
API.add_resource(App,"/app")
API.add_resource(Usage_Docu,"/api-docu")
API.add_resource(Technical_Docu,"/api-tech")
API.add_resource(Imprint,"/imprint")


# def refresh_model():
#     for i in range(1,2):
#         i=str(i)
#         Scraper.scrape(i)
#         Scraper.merge(i)
#         PreProcessor.clean_files(i)
#         Trainer.update_ar_model(i,intervall=5*4*24,start_lag= 1,end_lag= 680,start_skip= 227805,end_skip= -1)

if __name__=="__main__":
    day_intervall_for_schedule = 35
    # SCHEDULER.add_job(id="Scheduled task", func=refresh_model, trigger="interval", seconds=day_intervall_for_schedule*86400)
    # SCHEDULER.start()
    APP.run(debug=False)