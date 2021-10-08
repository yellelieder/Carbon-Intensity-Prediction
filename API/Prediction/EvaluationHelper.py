from datetime import datetime, timedelta
import pandas as pd
from random import randint, seed

def period_to_time(period, start):
    return (datetime.strptime(start, '%d/%m/%Y %H:%M:%S')+timedelta(seconds=period*900)).strftime('%d/%m/%Y %H:%M:%S')

def time_to_period(time,type):
    input_time_index=datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    base_time_index = get_last_date(type=type)
    #base_time_index=datetime.strptime("14/09/2021 23:45:00", '%d/%m/%Y %H:%M:%S')
    return int(divmod((input_time_index-base_time_index).total_seconds(),900)[0])-1

def get_last_date(type:str):
    path = f"Ressources\TrainingData\{type.capitalize()}.pkl"
    df=pd.read_pickle(path)
    return df.iloc[-1,0]

def get_production_consumption_ratio(start, end):
    production_prediction=pd.read_pickle("Ressources\TrainingData\Production.pkl")[time_to_period(start,"Production"):time_to_period(end,"Production")+1]["Production"]
    consumption_prediction=pd.read_pickle("Ressources\TrainingData\Consumption.pkl")[time_to_period(start,"Consumption"):time_to_period(end,"Consumption")+1]["Consumption"]
    return production_prediction.divide(other=consumption_prediction).to_frame()

def find_optimum(time_series, duration, start):
    norm_duration=int(duration/15)
    max_cummulative_ratio=0
    optimal_period=0
    for period in range(time_series.size-norm_duration):
        subset_sum=sum(time_series.iloc[period: period+norm_duration].values)
        if subset_sum>max_cummulative_ratio:
            max_cummulative_ratio=subset_sum
            optimal_period=period
    return period_to_time(optimal_period, start)


def get_randome(time_series, start, dur):
    norm_duration=int(dur/15)
    seed(time_series.size)
    optimal_period=randint(1, time_series.size-norm_duration)
    return period_to_time(optimal_period, start)


def run (start, end, dur):
    time_series = get_production_consumption_ratio(start, end)
    return find_optimum(time_series, dur,start), get_randome(time_series, start, dur)

if __name__=="__main__":
    time_series = get_production_consumption_ratio("21/07/2021 07:30:00", "24/07/2021 13:30:00")
    print(find_optimum(time_series, 120,"21/07/2021 07:30:00"))