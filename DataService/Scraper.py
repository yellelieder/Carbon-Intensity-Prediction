from selenium import webdriver

def getUrl(category, start, end):
    return "https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B\"selectedCategory\":"+category+",\"selectedSubCategory\":1,\"selectedRegion%\":\"DE\",\"from\":"+start+",\"to\":"+end+",\"selectedFileType\"CSV\"%7D"

driver = webdriver.Chrome()
driver.get(getUrl(1,1625090400000,1625263199999))