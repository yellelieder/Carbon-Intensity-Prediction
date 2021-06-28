from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api=Api(app)

class prediction(Resource):
    def get(self):
        return

api.add_resource(prediction,"/")
