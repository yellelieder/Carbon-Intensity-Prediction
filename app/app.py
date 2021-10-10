from flask import Flask
from flask_restful import Api
from app import routes
from flask_apscheduler import APScheduler, scheduler
import config
import logger as log
from app.data import scraper


APP = Flask(__name__)
API = Api(APP)
log.add.info(f"app is booted")

#setup routes for html pages
API.add_resource(routes.EPI,"/api/")
API.add_resource(routes.TestEndpoint,"/test/")
API.add_resource(routes.Home,"/")
API.add_resource(routes.App,"/app")
API.add_resource(routes.Usage_Docu,"/api-docu")
API.add_resource(routes.Technical_Docu,"/api-tech")
API.add_resource(routes.Imprint,"/imprint")
log.add.info(f"handlers added")

#setup scheduler for scraping and re-training of machine learning models
SCHEDULER=APScheduler()
SCHEDULER.add_job(id="Scheduled task", func=scraper.run, trigger="interval", seconds=120)#config.day_intervall_for_schedule*86400)
SCHEDULER.start()
log.add.info(f"scheduler started")

APP.run(debug=False)




