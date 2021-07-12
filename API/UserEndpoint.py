from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import Prediction


app=Flask(__name__)
api=Api(app)
    
class EPI(Resource):
    def get(self):
        start="08/07/2021 07:00:00"
        end="08/07/2021 11:00:00"
        dur=90
        return jsonify({"ideal start":Prediction.predict(start, end, dur)}), 200

#?lat=51.4582235&long=7.0158171&stdate=28.12.1995&sttime=06:455&endate=29.12.1995&entime=23:59&dur=180
api.add_resource(EPI,"/api/")

if __name__=="__main__":
    app.run(debug=True)