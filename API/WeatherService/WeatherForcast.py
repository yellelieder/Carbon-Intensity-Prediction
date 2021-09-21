import logging
import requests
import json
import logging
from datetime import datetime
import math
WEATHER_DATA_API_KEY="89f83e40489b5e87c4cb16463dc68b42"

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler=logging.FileHandler("logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(funcName)s:%(message)s"))
log.addHandler(handler)

def parser(s):
    '''
    Parses dates from csv into date object.

        Parameters:
        ----------
        s : str
            Timestapm in csv

        Returns:
        ----------
        date : datetime
            Object of form dd/mm/yyyy hh:mm:ss
    '''
    return datetime.strptime(s,"%d/%m/%Y %H:%M:%S")

def get_url(lat, lng):
    '''
    Turns geo-coordinates in weather api url.

        Parameters:
        ----------

        lat : str
            Lattitude of the place where energy is going to be consumed.

        lng : str
            Longitude of the place where energy is going to be consumed.

        Returns:
        ----------

        url : str
            Url with correct parameter for requesting weather data.yoy
    '''
    #starts at last full hour, if it is 7:30 now, first return is 6
    log.info(f"converting {lat} and {lng} to weather api url")
    return f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lng}&units=metric&appid={WEATHER_DATA_API_KEY}"


#https://openweathermap.org/api/one-call-api
def get_forcast(lat, lng, hours_from_now, hours_total):
    '''
    Turns geo-coordinates in weather forcast.

        Parameters:
        ----------

        lat : str
            Lattitude of the place where energy is going to be consumed.

        lng : str
            Longitude of the place where energy is going to be consumed.

        Returns:
        ----------

        response : str
            Weather forcast for wind and sun, for timeframe requested.
    '''
    #start und ende in unix
    log.info(f"request weather api")
    #response=requests.get(get_url(lat,lng)).json()
    return requests.get(get_url(lat,lng)).json()["list"]
    #[hours_from_now:hours_from_now+hours_total]

def get_best_start(lat, lon, start:str, end:str, dur:int):
    dur_in_hours = math.ceil(dur/60)
    start_in_hours = (parser(start)-datetime.now())
    days, seconds = start_in_hours.days, start_in_hours.seconds
    start_in_hours = days * 24 + seconds
    hours_total = (parser(end)-parser(start))
    days, seconds = hours_total.days+1, hours_total.seconds
    hours_total = days * 24 + seconds
    
    pred=get_forcast(lat,lon, start_in_hours,hours_total+1)
    max_wind_speed = 0
    max_wind_day = 0
    min_cloudiness= math.inf
    min_cloud_day = 0
    #a very simple solution in lack of proper domain knowledge
    for hour in range(len(pred)-dur_in_hours):
        print(hour)
        subset_sum_wind=0
        subset_sum_clouds=0
        for hour_in_subset in pred[hour:hour+dur_in_hours]:
            subset_sum_wind +=hour_in_subset["speed"]
            subset_sum_clouds +=hour_in_subset["clouds"]
        if subset_sum_wind>max_wind_speed:
            max_wind_day=hour
            max_wind_speed=subset_sum_wind
        if subset_sum_wind<min_cloudiness:
            min_cloud_day=hour
            min_cloudiness=subset_sum_clouds
    start_hour = min(max_wind_day, min_cloud_day)
    surise=datetime.utcfromtimestamp(pred[start_hour]["sunrise"]).strftime('%H:%M')
    return datetime.utcfromtimestamp(pred[start_hour]["dt"]).strftime('%d/%m/%Y')+" "+surise +":00"

if __name__=="__main__":
    #nur wenn Anfrage in den nächsten 30 Tage
    #dann genau für den Zeitraum
    #print(json.dumps(get_forcast("51.4582235","7.0158171", 3,2), indent=1))
    # forcast = get_forcast("51.4582235","7.0158171", 3,5)
    # for i in forcast:
    #     print("\nTime: ",datetime.utcfromtimestamp(i["dt"]).strftime('%d.%m.%Y %H:%M'))
    #     print("Cloudiness: ",i["clouds"]["all"],"%")
    #     print("Wind: ",i["wind"]["speed"],"meters/second")
    print(get_best_start("51.4582235","7.0158171","22/09/2021 21:30:00", "23/09/2021 04:20:00", 360))