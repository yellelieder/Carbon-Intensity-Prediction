from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime
import regex as re
import time
import pandas as pd
from app.data import preprocessor
import logging
from app.helpers import common
from app.machinelearning import trainer
import config
import logger as log

def get_url(type:str, start:str, end:str):
    '''
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
    '''
    log.add.info(f"creating smard.de url from type: {type}, start: {start}, end: {end}")
    if type=="1":
        sub="1"
    else:
        sub="5"
    return f"https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:{type},%22selectedSubCategory%22:{sub},%22selectedRegion%22:%22DE%22,%22from%22:{start},%22to%22:{end},%22selectedFileType%22:%22CSV%22%7D"

def get_next_date(type:str):
    '''
    Returns first date for which market data is not already persistet. 

        Parameters:
        ----------

        type : str
            The type of data. 1=production, 2=consumption

        Returns:
        ----------

        date : str
            Date for which market data is missing. 
    '''
    log.add.info(f"calculating date, where to start scraping")
    path = get_download_path(type)
    filename = common.get_latest_file(path)
    x= filename.split("_")[3]
    return str(time.mktime(datetime.strptime(x.split(".")[0], "%Y%m%d%H%M").timetuple())+86400).split(".")[0]+"000"

def get_last_date(type:str, days):
    path = get_download_path(type)
    filename = common.get_latest_file(path)
    x= filename.split("_")[3]
    return str(time.mktime(datetime.strptime(x.split(".")[0], "%Y%m%d%H%M").timetuple())+days*86400).split(".")[0]+"000"

def get_download_path(type:str):
    '''
    Returns folder path for downloaded files by data type. 

        Parameters:
        ----------

        type : str
            The type of data. 1=production, 2=consumption

        Returns:
        ----------

        path : str
            Relative folder path for downloaded data.
    '''
    return "Ressources\Downloads\Production" if type=="1" else "Ressources\Downloads\Consumption"

def scrape(type:str):
    '''
    Scrapes most recent electricity market data.

        Parameters:
        ----------

        type : str
            The type of data. 1=production, 2=consumption

        Returns:
        ----------
        
        Persists data as csv in projects download folder.
    '''
    log.add.info(f"scraping new date from smard.de for type {type}")
    start_period=get_next_date(type)
    end_period=get_last_date(type, config.scrape_days)
    options=webdriver.ChromeOptions()
    t="\Production" if type=="1" else"\Consumption"
    preferences={"download.default_directory":config.local_path+r"\EPI\Ressources\Downloads"+t}
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(get_url(type,start_period,end_period))
    driver.find_element(By.XPATH,"//*[@id=\"help-download\"]/button").click()
    time.sleep(5)
    driver.close()
    driver.quit()

def merge(type):
    '''
    Merges all existing downloads of same type to single csv.

        Parameters:
        ----------
        
        dir : str
            Folder path from where to merge files.

        Returns:
        ----------
        
        Persists result as single csv at Ressources\RawDataMerged
    '''
    dir="Ressources\Downloads\Production" if type=="1" else "Ressources\Downloads\Consumption"
    log.add.info(f"merging files from folder: {dir}")
    data=pd.DataFrame()
    for i in os.listdir(dir):
        file=pd.read_csv(dir+"\\"+i, sep=";", dtype=str)
        data=data.append(file, ignore_index=True)
    df = pd.DataFrame(data)
    df.to_csv("Ressources\\RawDataMerged\\"+dir.split("\\")[2]+".csv")
    df.to_pickle("Ressources\\RawDataMerged\\"+dir.split("\\")[2]+".pkl")

def run():
    for i in range(1,2):
        lag = config.production_training_lags if i==1 else config.consumption_training_lags
        i=str(i)
        scrape(i)
        merge(i)
        preprocessor.clean_files(i)
        trainer.update_ar_model(i,intervall=config.rmse_intervall,start_lag= lag-1,end_lag= lag+1,start_skip= config.model_skip_row_start,end_skip= -1)
