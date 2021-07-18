from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def getUrl(category:str, start:str, end:str):
    return "https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:"+category+",%22selectedSubCategory%22:1,%22selectedRegion%22:%22DE%22,%22from%22:"+start+",%22to%22:"+end+",%22selectedFileType%22:%22CSV%22%7D"

driver = webdriver.Chrome(ChromeDriverManager().install())
#
driver.get(getUrl("1","1625695200000","1625867999999"))

'''1625695200000,"to":1625867999999
08.07.21 bis 09.07.21

:1625090400000,"to":1625263199999,"
01.07 bis 02.07'''

