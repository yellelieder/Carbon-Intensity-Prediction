#api key to access paid weather forcast service, they offer a free students access
from werkzeug.wrappers import response


openweathermap_org_api_key="89f83e40489b5e87c4cb16463dc68b42"

#google maps api key
googlemaps_api_key ="AIzaSyCBkqBTgj99v45ScAWO-2A3Ffz8r0kQbc8"

#no. of intervalls that should be looked at for calculation models rmse
rmse_intervall = 5*4*24 #5 days, 4*15m per hour, 24 hours = 5 days

#no. of n intervalls to be concidered when predicting lag n+1
production_training_lags = 275
consumption_training_lags = 674

#starting row from where the model should not know the data
model_skip_row_start = 227805

#path where EPI project is located ..\EPI\.., excluding last backslash
local_path=r"C:\Users\liede\OneDrive\Studium\BP - Bachelor Project"

#project folder pahts
model_production_folder="Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionProduction\\"
model_consumption_folder ="Ressources\Models\ModelsAutoRegression\ModelsAutoRegressionConsumption\\"
model_folder ="Ressources\Models\ModelsAutoRegression\\"
training_data_folder="Ressources\TrainingData\\"
merged_data_folder="Ressources\RawDataMerged\\"
download_production_folder="Ressources\Downloads\Production" 
download_consumption_folder="Ressources\Downloads\Consumption" 

#default date format to be used in the system
dateformat='%d/%m/%Y %H:%M:%S'

#how often (every n days) the scheduler should be executed
#the fresher the training date, the better the prediction
day_intervall_for_schedule = 7

#how many days should be scraped in one sitting
scrape_days=7
