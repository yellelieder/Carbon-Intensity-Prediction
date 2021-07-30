from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime
import regex as re
import time
import pandas as pd
import PreProcessor
import logging

TIME_STAMP = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

def getLatestFile(dir):
    '''
    Returns last file form folder by alphabetical order.

        Parameters:
        ----------

        dir : str
            Folder to search from.

        Returns:
        ----------

        file_name : str
            Name of the last file from the folder in alphabetical order.
    '''
    return sorted(os.listdir(dir)).pop()

def getUrl(type:str, start:str, end:str):
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
    log.info(f"creating smard.de url from type: {type}, start: {start}, end: {end}")
    if type=="1":
        sub="1"
    else:
        sub="5"
    return f"https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:{type},%22selectedSubCategory%22:{sub},%22selectedRegion%22:%22DE%22,%22from%22:{start},%22to%22:{end},%22selectedFileType%22:%22CSV%22%7D"

def getNextDate(type:str):
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
    log.info(f"calculating date, where to start scraping")
    path = getDownloadPath(type)
    filename = getLatestFile(path)
    x= filename.split("_")[3]
    return str(time.mktime(datetime.strptime(x.split(".")[0], "%Y%m%d%H%M").timetuple())+86400).split(".")[0]+"000"

def getDownloadPath(type:str):
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
    if type=="1":
        return "Ressources\Downloads\Production"
    else:
        return "Ressources\Downloads\Consumption"

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
    log.info(f"scraping new date from smard.de for type {type}")
    no_of_days_to_get=7
    start_period=getNextDate(type)
    end_period=str(float(start_period)+(86400*no_of_days_to_get)).split(".")[0]
    options=webdriver.ChromeOptions()
    if type=="1":
        t="\Production"
    else: 
        t= "\Consumption"

    '''There is unfortunately no way to make this path relative with selenium.
    But selenium is needed, as the scraped site is build dynamically.'''

    preferences={"download.default_directory":r"C:\Users\liede\OneDrive\Studium\BP - Bachelor Project\EPI-Project\Ressources\Downloads"+t}
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(getUrl(type,start_period,end_period))
    driver.find_element(By.XPATH,"//*[@id=\"help-download\"]/button").click()
    #should validate column names here
    time.sleep(5)
    driver.close()
    driver.quit()

def merge(dir):
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
    log.info(f"merging files from folder: {dir}")
    data=pd.DataFrame()
    for i in os.listdir(dir):
        file=pd.read_csv(dir+"\\"+i, sep=";")
        data=data.append(file, ignore_index=True)
    df = pd.DataFrame(data)
    #must handle existance of multiple files in this fol
    df.to_csv("Ressources\\RawDataMerged\\"+dir.split("\\")[2]+".csv")

if __name__=="__main__":
    start = time.time()
    scrape("1")
    end1 = time.time()
    print("first scraping took: ", end1-start)
    scrape("2")
    end2 = time.time()
    print("second scraping took: ", end2-end1)
    merge(getDownloadPath("1"))
    end3 = time.time()
    print("first merging took: ", end3-end2)
    merge(getDownloadPath("2"))
    end4 = time.time()
    print("second merging took: ", end4-end3)
    PreProcessor.clean("1")
    end5 = time.time()
    print("first cleaning took: ", end5-end4)
    PreProcessor.clean("2")
    end6 = time.time()
    print("second cleaning took: ", end6-end5)
    print("\ntotal scrapting time: ", end6-start)
