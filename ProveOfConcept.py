from flask_apscheduler.api import run_job
import requests
from flask import Flask
from flask_apscheduler import APScheduler
from datetime import date, datetime, timedelta


APP = Flask(__name__)
@APP.route("/")
def index():
    return "hi"

memory_with_api = 0
memory_without_api=0
cpu_with_api=0
cpu_without_api=0

delay=3
SCHEDULER=APScheduler()
now=datetime.now()
stdate=now.date().strftime("%d/%m/%Y")
sttime= (now + timedelta(minutes=delay)).strftime("%H:%M")
enddate=stdate
endtime=(now + timedelta(minutes=(delay+16))).strftime("%H:%M")

response=requests.get(f"http://127.0.0.1:5000/api/?lat=50.9917119&long=10.2136589&stdate={stdate}&sttime={sttime}&endate={enddate}&entime={endtime}&dur=15").json()["ideal start"]

start_time= datetime.strptime(response,"%d/%m/%Y %H:%M:%S")
def scheduled_task():
    print("calculating job: ",datetime.now())
    #source: https://www.programiz.com/python-programming/examples/multiply-matrix
    # Program to multiply two matrices using list comprehension
    # 3x3 matrix
    X = [[12,7,3],
        [4 ,5,6],
        [7 ,8,9]]

    # 3x4 matrix
    Y = [[5,8,1,2],
        [6,7,3,0],
        [4,5,9,1]]

    # result is 3x4
    result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]
    for r in result:
        print(r)

def with_api():
    SCHEDULER.add_job(id="Scheduled task", func=scheduled_task, trigger="date", next_run_time=start_time)
    SCHEDULER.start()

def without_api():
    scheduled_task()

def run_app():
    without_api()
    with_api()
    APP.run(debug=True)
    
if __name__=="__main__":
    run_app()