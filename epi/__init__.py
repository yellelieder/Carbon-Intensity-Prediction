from flask import Flask
from flask_restful import Api
from flask_apscheduler import APScheduler
from epi import config
from epi.data import scraper
from epi import logger as log
from epi import routes

app = Flask(__name__)
api = Api(app)
log.add.info("app is booted")



# setup routes for html pages
api.add_resource(routes.EPI, "/api/")
api.add_resource(routes.TestEndpoint, "/test/")
api.add_resource(routes.Home, "/")
api.add_resource(routes.App, "/app")
api.add_resource(routes.Usage_Docu, "/api-docu")
api.add_resource(routes.Imprint, "/imprint")
log.add.info("handlers added")

# setup scheduler for scraping and re-training of machine learning models
scheduler = APScheduler()
# everything afer "seconds=" can just be set to ~120 for testing purposes
scheduler.add_job(
    id="Scheduled task",
    func=scraper.run,
    trigger="interval",
    seconds=config.scheduler_intervall_days * 60 * 60 * 24,
)  # 60sec*60min*24h
scheduler.start()  # first execution always after itervall passed first time
log.add.info("scheduler started")
