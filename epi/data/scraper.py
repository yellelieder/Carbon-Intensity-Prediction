from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime, timedelta
import time
import pandas as pd
from epi.data import preprocessor
from epi.helpers import common
from epi.machinelearning import trainer
from epi import config
from epi import logger as log


def _get_url(type: str, start: str, end: str):
    """
    Turns start and end time into electricity marked data api url.

        Parameters:
        ----------

            start : str
                First date for which data must be scraped.

            end : str
                Last data from which data must be scraped.

            type : str
                The type of data. 1=production, 2=consumption

        Returns:
        ----------

            url : str
                Url with correct parameter for requesting electricity market data.
    """
    # sub-typed distinct between smard.de prognose and actual numbers
    if type == config.p_id:
        sub_type = "1"
    else:
        sub_type = "5"
    url = f"https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:{type},%22selectedSubCategory%22:{sub_type},%22selectedRegion%22:%22DE%22,%22from%22:{start},%22to%22:{end},%22selectedFileType%22:%22CSV%22%7D"
    log.add.info(f"smard.de url type {type} created, start: {start}, end: {end}")
    return url


def _get_next_date(type: str):
    """
    Returns first date for which market data is not already persistet. 

        Parameters:
        ----------

            type : str
                The type of data 1=Production, 2=Consumption.

        Returns:
        ----------

            date : str
                Date for which market data is missing. 
    """
    path = (
        config.download_production_folder
        if type == config.p_id
        else config.download_consumption_folder
    )
    filename = common.get_latest_file(path)
    file_name_last_element = filename.split("_")[3]
    date = (
        str(
            time.mktime(
                datetime.strptime(
                    file_name_last_element.split(".")[0], "%Y%m%d%H%M"
                ).timetuple()
            )
            + 86400
        ).split(".")[0]
        + "000"
    )
    log.add.info(f"calculated last date where training date exists: {date}")
    return date


def _get_last_date(type: str):
    """
    Returns date up to which new data should be scrapet.

        Parameters:
        ----------

            type : str
                The type of data 1=Production, 2=Consumption.

        Returns:
        ----------

            date : str 
                Date which should still be included in next scraping activity. 
    """
    path = (
        config.download_production_folder
        if type == config.p_id
        else config.download_consumption_folder
    )
    filename = common.get_latest_file(path)
    file_name_last_element = filename.split("_")[3]
    date = (
        str(
            time.mktime(
                datetime.strptime(
                    file_name_last_element.split(".")[0], "%Y%m%d%H%M"
                ).timetuple()
            )
            + config.scheduler_intervall_days * 86400
        ).split(".")[0]
        + "000"
    )
    log.add.info(f"calculated date up to which should be scraped: {date}")
    return date


def _scrape(type: str):
    """
    Scrapes most recent electricity market data.

        Parameters:
        ----------

        type : str
            The type of data 1=Production, 2=Consumption.

        Returns:
        ----------
        
            None : Persists data as csv in projects download folder.
    """
    start_period = _get_next_date(type)
    end_period = _get_last_date(type)
    # selenium/XPATH as page is single page applikation and buttons got no css IDs
    options = webdriver.ChromeOptions()
    download_path = (
        config.download_production_folder
        if type == config.p_id
        else config.download_consumption_folder
    )
    preferences = {
        "download.default_directory": config.local_path
        + f"EPI{config.slash}"
        + download_path
    }
    # experimental options to not use default download folder
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(_get_url(type, start_period, end_period))
    try:
        driver.find_element(By.XPATH, '//*[@id="help-download"]/button').click()
    except Exception:
        print(
            "Element on smard.de could not be found, please readjust XPATH element and check website manually."
        )
    finally:
        time.sleep(5)
        driver.close()
        driver.quit()
    log.add.info(f"scraping for type {type} completed")


def _merge(type: str):
    """
    Merges all existing downloads of same type to single file.

        Parameters:
        ----------
        
            type : str
                Type of the date to be merged 1=Production, 2=Consumption.

        Returns:
        ----------
        
            None : Persists result as csv and pkl at Ressources\RawDataMerged
    """
    dir = (
        config.download_production_folder
        if type == config.p_id
        else config.download_consumption_folder
    )
    data = pd.DataFrame()
    try:
        for file in os.listdir(dir):
            content = pd.read_csv(dir + config.slash + file, sep=";", dtype=str)
            data = data.append(content, ignore_index=True)
    except FileNotFoundError as exception:
        common.print_fnf(dir, exception)
    df = pd.DataFrame(data)
    file_name = config.merged_data_folder + (config.c if type == config.c_id else config.p)
    df.to_csv(file_name + ".csv")
    df.to_pickle(file_name + ".pkl")
    log.add.info(f"files from {dir} merged and persisted at {file_name}")


def run():
    """
    Initializes the machine learning pipeline.

    Runs the scraper, merges no data into existing, cleans data and re-trains models for production and consumption.

        Parameters:
        ----------

            None : Uses files in static directories.

        Returns:
        ----------

            None : Stores models in static directories.
    """
    # if common.str_to_datetime(common.last_training_date)
    last_production_as_dt = common.str_to_datetime(common.last_training_date(config.p))
    last_consumption_as_dt = common.str_to_datetime(common.last_training_date(config.c))
    scraping_threshold_date = datetime.now() - timedelta(
        days=(config.scheduler_intervall_days) + 1
    )
    if (
        last_production_as_dt < scraping_threshold_date
        and last_consumption_as_dt < scraping_threshold_date
    ):
        for type in range(1, 3):
            lag = config.production_lags if type == 1 else config.consumption_lags
            type = str(type)
            _scrape(type)
            _merge(type)
            preprocessor.clean_file(type)
            trainer.update_ar_model(
                type,
                intervall=config.rmse_intervall,
                start_lag=lag - 1,
                end_lag=lag + 1,
                start_skip=config.model_skip_row_start,
            )
            log.add.info(f"scraping, cleaning, merging, training done for type {type}")
    else:
        log.add.info("tried scraping, data is up to date")
