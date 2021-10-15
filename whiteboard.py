from datetime import datetime, timedelta
from epi import config
from epi.helpers import common
import regex as re
import pandas as pd
import os
from epi import logger as log
from epi.data import preprocessor

last_production_as_dt=common.str_to_datetime(common.last_training_date(config.p))
last_consumption_as_dt=common.str_to_datetime(common.last_training_date(config.c))
scraping_threshold_date=(datetime.now()-timedelta(days=(config.scrape_days)+1))
if last_production_as_dt< scraping_threshold_date and last_consumption_as_dt<scraping_threshold_date:
    print(True)
