from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
from datetime import datetime
import regex as re
import time
DOWNLOAD_DIR="Ressources\Downloads"
start_period="1625695200000"
end_period="1625867999999"

timeStamp = re.sub('[-:. ]', '_', str(datetime.now().strftime("%Y-%m-%d %H:%M")))

def getLatestFile(dir):
    return sorted(os.listdir(dir)).pop()

def getUrl(category:str, start:str, end:str):
    return "https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:"+category+",%22selectedSubCategory%22:1,%22selectedRegion%22:%22DE%22,%22from%22:"+start+",%22to%22:"+end+",%22selectedFileType%22:%22CSV%22%7D"

def getNextDate(type:str):
    path = getDownloadPath(type)
    #filename = max([path + "\\" + f for f in os.listdir(path)],key=os.path.getctime)
    filename = getLatestFile(path)
    x= filename.split("_")[3]
    return str(time.mktime(datetime.strptime(x.split(".")[0], "%Y%m%d%H%M").timetuple())+86400).split(".")[0]+"000"

def getDownloadPath(type:str):
    if type=="1":
        return "Ressources\Downloads\Production"
    else:
        return "Ressources\Downloads\Consumption"

def scrape(type:int):
    '''Type 1 for production, 2 for consumption'''
    no_of_days_to_get=1
    start_period=getNextDate(type)
    end_period=str(float(start_period)+(86400*no_of_days_to_get)).split(".")[0]
    options=webdriver.ChromeOptions()
    preferences={"download.default_directory":r"C:\Users\liede\OneDrive\Studium\BP - Bachelor Project\EPI-Project\Ressources\Downloads"}
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(getUrl(type,start_period,end_period))
    driver.find_element(By.XPATH,"//*[@id=\"help-download\"]/button").click()
    time.sleep(5)
    #filename = max([DOWNLOAD_DIR + "\\" + f for f in os.listdir(DOWNLOAD_DIR)],key=os.path.getctime)
    #shutil.move(filename,os.path.join(DOWNLOAD_DIR,"download_"+start_period+"_"+end_period+"_"+timeStamp+".csv"))
    driver.close()
    driver.quit()
1625833622
1625920022

if __name__=="__main__":
    #print(getNextDate("1"))
    scrape("1")
