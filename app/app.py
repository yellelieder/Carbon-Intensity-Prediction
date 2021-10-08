from flask import Flask
from flask_restful import Api
from app import routes

APP = Flask(__name__)
API = Api(APP)

API.add_resource(routes.EPI,"/api/")
API.add_resource(routes.TestEndpoint,"/test/")
API.add_resource(routes.Home,"/")
API.add_resource(routes.App,"/app")
API.add_resource(routes.Usage_Docu,"/api-docu")
API.add_resource(routes.Technical_Docu,"/api-tech")
API.add_resource(routes.Imprint,"/imprint")
APP.run(debug=False)
