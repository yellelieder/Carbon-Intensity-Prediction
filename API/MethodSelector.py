import math
from datetime import datetime
import Prediction
#from WeatherForcast import WeatherForcast
#from WeatherForcast import ClimateForcast

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

def select_method(lat, lng, start, end, dur):
    days_in_future=parser(start)-datetime.now().days
    #next hour
    return Prediction.get_best_start(start, end, dur)
    
    if(days_in_future<30):
        if(days_in_future<4):
            return 
        else:
            if(math.ceil(dur/24))<24:
                return Prediction.get_best_start(start, end, dur)
            else:
                return ClimateForcast.get_best_start(lat, lng, start, end, dur)
    else:
        return Prediction.get_best_start(start, end, dur)



    #next four days

    #else
    ...
