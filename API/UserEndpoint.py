from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import Prediction
from datetime import datetime
import regex as re
import requests
import json
from flask_apscheduler import APScheduler


app=Flask(__name__)
api=Api(app)
scheduler=APScheduler()
    
class EPI(Resource):
    def get(self):
        """Handles users get request with prediction in form of json."""
        try:
            query=request.args 
            start=to_timestamp(query.get("stdate"),query.get("sttime"))
            end=to_timestamp(query.get("endate"),query.get("entime"))
            dur=int(query.get("dur"))
            lat=float(query.get("lat"))
            lng=float(query.get("long"))
            if dur<15:
                return {"error":"duration must be minimum of 15 min"}, 406 
            elif start_after_end(start, end):
                return {"error":"end before start"}, 406 
            elif start_in_past(start):
                return {"error":"enter upcoming timeframe"}, 406  
            elif time_le_dur(start, end, dur):
                return {"error":"duration not fitting in timeframe"}, 406
            elif lat<-90 or lat>90:
                return {"error":"lattitude out of rang"}, 406
            elif lng<-180 or lng>180:
                return {"error":"longitude out of range"}, 40
            elif invalid_geo(query.get("lat"), query.get("long")):  
                return {"error":"enter german coodrinates"}, 406  
            else:
                return {"ideal start":Prediction.timeStamp(start, end, dur)}, 200
        except:
            return {"error":"invalid input"}, 406

class Home(Resource):
    def get(self):
        """Returns instruction to use /api/ from home directory."""
        return "please send your GET to /api/ for a prediction", 200

def to_timestamp(date, time):
    """Converts 'Date' and 'Time' strings into properly formated datetime string."""
    return str(re.sub("[.]","/", date)+" "+time+":00")

def start_after_end(start, end):
    """Returns true, if start date is later then end date."""
    return datetime.strptime(start, '%d/%m/%Y %H:%M:%S')>datetime.strptime(end, '%d/%m/%Y %H:%M:%S')

def start_in_past(start):
    """Returns true if start date is already passed."""
    return datetime.strptime(start, '%d/%m/%Y %H:%M:%S')<datetime.now()

def time_le_dur(start, end, dur):
    """Returns true if dur(ation) does not fit in range between start and end."""
    return not int(divmod((datetime.strptime(end, '%d/%m/%Y %H:%M:%S')-datetime.strptime(start, '%d/%m/%Y %H:%M:%S')).total_seconds(),900)[0])>=int(dur/15)

def invalid_geo(lat, lng):
    """Returns true if geo coordinates are outside of Germany."""
    response=requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","
    +lng+"&result_type=country&key=AIzaSyCBkqBTgj99v45ScAWO-2A3Ffz8r0kQbc8").json()["results"][0]["formatted_address"]
    if response=="Germany":
        return False
    else:
        return True

#?lat=51.4582235&long=7.0158171&stdate=28.12.1995&sttime=06:45&endate=29.12.1995&entime=23:59&dur=180
api.add_resource(EPI,"/api/")
api.add_resource(Home,"/")

def scheduledTask():
    print("Task executed")

if __name__=="__main__":
    scheduler.add_job(id="Scheduled task", func=scheduledTask, trigger="interval", seconds=86400)
    scheduler.start()
    app.run(debug=True)