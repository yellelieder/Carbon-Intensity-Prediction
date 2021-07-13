from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import Prediction
from datetime import datetime
import regex as re


app=Flask(__name__)
api=Api(app)
    
class EPI(Resource):
    def get(self):
        query=request.args 
        start=to_timestamp(query.get("stdate"),query.get("sttime"))
        end=to_timestamp(query.get("endate"),query.get("entime"))
        dur=int(query.get("dur"))
        if dur<15:
            return {"error":"duration must be minimum of 15 min"}, 406 
        elif start_after_end(start, end):
            return {"error":"end before start"}, 406 
        elif start_in_past(start):
            return {"error":"enter upcoming timeframe"}, 406  
        elif time_le_dur(start, end, dur):
            return {"error":"duration not in limits"}, 406
        elif invalid_geo(query.get("lat"), query.get("long")):  
            return {"error":"enter german coodrinates"}, 406  
        else:
            return {"ideal start":Prediction.timeStamp(start, end, dur)}, 200

class Home(Resource):
    def get(self):
        return "please send your GET to /api/ for a prediction", 200

def to_timestamp(date, time):
    return str(re.sub("[.]","/", date)+" "+time+":00")

def start_after_end(start, end):
    return datetime.strptime(start, '%d/%m/%Y %H:%M:%S')>datetime.strptime(end, '%d/%m/%Y %H:%M:%S')

def start_in_past(start):
    return datetime.strptime(start, '%d/%m/%Y %H:%M:%S')<datetime.now()

#doese not work yet
def time_le_dur(start, end, dur):
    return int(divmod((datetime.strptime(end, '%d/%m/%Y %H:%M:%S')-datetime.strptime(start, '%d/%m/%Y %H:%M:%S')).total_seconds(),900)[0])>=dur

def invalid_geo(lat, long):
    #todo- google validation
    return False

#?lat=51.4582235&long=7.0158171&stdate=28.12.1995&sttime=06:455&endate=29.12.1995&entime=23:59&dur=180
api.add_resource(EPI,"/api/")
api.add_resource(Home,"/")

if __name__=="__main__":
    app.run(debug=True)