# EPI
Electricity Prediction Interface

Welcome to the EPI project!

The goal of this project is to provide software engineers with a simple solution to concider carbon emission in their application development.

## WHY IT'S WORTH IT
- software is responsible for at least 3% of world carbon emission
- using renevables, if possible has the potential to drastically reduce this

## HOW IT WORKS:
- we have gathered electricity market data (and continue scraping the most current ones)
- we concider weather forcasts (for predictions within the next 30 days)
- we make predictions for future availability of renevable energy
- this way we enable you to run ressource intensive processes when ther is a high probability for an green energy surplus

## HOW TO USE IT
- make a call to /api/?lat=51.4582235&long=7.0158171&stdate=28.12.2021&sttime=06:45&endate=29.12.2021&entime=23:59&dur=180
- lat is the lattitue of where the electricity is going to be consumed
- lng is the longitude
- stdate is the earliest possible date for the process to be started
- sttime is the time
- endate is the date when the process latest must be finished
- entime is the latest time
- dur is the approximate duration of your process in minutes

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
