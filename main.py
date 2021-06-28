from flask import Flask, request
from flask import json
from flask.helpers import make_response
from flask.json import jsonify

app = Flask(__name__)

PORT = 5000
HOST="0.0.0.0"

@app.route("/")
def index():
    return jsonify({"error":"please call /api"})

@app.route("/api")
#?latitude=51.4582235&longitude=7.0158171&startdate=28.12.1995&starttime=06:455&enddate=29.12.1995&endtime=23:59&duration=180
def query_string():
    if request.args:
        req=request.args
        res={}
        for key, val in req.items():
            res[key]=val
        res=make_response(jsonify(res),200)
        return res
    res=make_response(jsonify({"error":"no query found"}))
    return res

if __name__=="__main__":
    app.run(host=HOST, port=PORT, debug=True)