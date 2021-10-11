# EPI
Electricity Prediction Interface

Welcome to the EPI project!

The goal of this project is to provide software engineers with a simple solution to concider carbon emission in their application development.

## HOW IT WORKS:
- we have gathered german* electricity market data (the system continues scraping current data)
- the system conciders weather forcasts (for predictions within the next 30 days)
- and makes predictions for future availability of renevable energy
- this enables you to run ressource intensive processes when ther is a high probability for an green energy surplus

## WHY IT'S WORTH IT
- software is responsible for at least 3% of world carbon emission
- using renevables, if possible has the potential to drastically reduce this

## HOW TO USE IT
- make a call to /api/?lat=51.4582235&long=7.0158171&stdate=28.12.2021&sttime=06:45&endate=29.12.2021&entime=23:59&dur=180
- lat = lattitue of where the electricity is going to be consumed (must be between -90 and +90)*
- lng = longitude (must be between -180 and +180)*
- stdate = earliest possible date for the process to be started (Format: DD.MM.YYYY)
- sttime = the time (Format: HH:MM)
- endate = date when the process latest must be finished
- entime = latest time
- dur = approximate duration of your process in minutes

Response will be a json like this: 

{
  "ideal start" : "01/01/2023 18:37:00"
}

## FIELDS OF APPLICATION
(just some inspiration for some processes where this can be used)
- database indexing
- backups
- synchronization
- training of machine learning models
- mining of crypto currency
- executing regression tests 
- rendering video 
- running deployment pipelines 
- automated processes like done with RPA
.. basically everything usually done overnight, where you don't really care when it's done 

*The system is only trained on german energy market data and therefore restricted to predictions for locations in Germany. Let me know if you have access to data for other locations.