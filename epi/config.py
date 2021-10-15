import platform
import os

"""EVERYTHING BELOW CAN BE CUSTOMIZED"""

# api key to access paid weather forcast service, they offer a free students access
openweathermap_key = "89f83e40489b5e87c4cb16463dc68b42"

# google maps api key
google_key = "AIzaSyCBkqBTgj99v45ScAWO-2A3Ffz8r0kQbc8"

# no. of intervalls that should be looked at for calculation models rmse
rmse_intervall = 5 * 4 * 24  # 5 days, 4*15m per hour, 24 hours = 5 days

# no. of n intervalls to be concidered when predicting lag n+1
production_lags = 275  # trial and error
consumption_lags = 674

# starting row from where the model should not know the data
model_skip_row_start = 227805
# everything after ~01.07.2021 is validation data this way

# how often (every n days) the scheduler should be executed
# the fresher the training date, the better the prediction
scheduler_intervall_days = 30


"""EVERYTHING BELOW SHOULD NOT BE CUSTOMIZED"""

# to promote interoperability
slash = "\\" if str(platform.system()) == "Windows" else "/"

# path where EPI project is located
local_path = str(os.getcwd().split("EPI")[0])

# project folder pahts
model_folder = f"epi{slash}ressources{slash}models{slash}modelsautoregression{slash}"
model_production_folder = f"{model_folder}modelsautoregressionproduction{slash}"
model_consumption_folder = f"{model_folder}modelsautoregressionconsumption{slash}"
training_data_folder = f"epi{slash}ressources{slash}trainingdata{slash}"
merged_data_folder = f"epi{slash}ressources{slash}rawdatamerged{slash}"
download_production_folder = f"epi{slash}ressources{slash}downloads{slash}production"
download_consumption_folder = f"epi{slash}ressources{slash}downloads{slash}consumption"
training_log_file = f"epi{slash}ressources{slash}models{slash}models.csv"

# default date format to be used in the system
dateformat = "%d/%m/%Y %H:%m:%S"

# commonly used keyword
p = "Production"
p_id = "1"
c = "Consumption"
c_id = "2"

