from datetime import datetime
import requests
from epi import config
from epi import logger as log


def start_after_end(start, end):
    """
    Checks if start and end time are compatible.
    Dates are not copatible if end is before start.

        Parameters:
        ----------
            start : str
                Ealiest time process can be started.
            
            end : str
                Latest time process must be finished.            

        Returns:
        ----------

            valitation : bool
                False if input is valid, True if input is invalid.
    """
    validation = datetime.strptime(start, config.dateformat) > datetime.strptime(end, config.dateformat)
    log.add.info(f"validation, {start} is after {end} = {validation}")
    return validation


def start_in_past(start):
    """
    Checks if user input is already in the past. 

        Parameters:
        ----------
            start : str
                Date to be validated. 

        Returns:
        ----------
            validation : bool
                False if input is valid, True if input is in the past.
    """
    validation = datetime.strptime(start, config.dateformat) < datetime.now()
    log.add.info(f"validation: {start} is before now = {not validation}")
    return validation


def time_le_dur(start, end, dur):
    """
    Checks if duration fits into given timeframe.

        Parameters:
        ----------

            start : str
                Where duration can start.
            
            end : str
                Where duration must end.

            dur : int
                Duration in minutes.

        Returns:
        ----------

            validation : bool
                False if input is valid, true if duration does not fit between start and end.
    """
    validation = not int(
        divmod(
            (
                datetime.strptime(end, config.dateformat)
                - datetime.strptime(start, config.dateformat)
            ).total_seconds(),
            900,
        )[0]
    ) >= int(dur / 15)
    log.add.info(
        f"validation: {dur}min. fits between {start} and {end} = {not validation}"
    )
    return validation


def invalid_geo(lat, lng):
    """
    Checks weather geo coordinates are in germany.

        Parameters:
        ----------

            lat : str
                Geographical lattitude.
            
            lng : str 
                Geographical longitude.

        Returns:
        ----------
        
            validation : bool
                False if coordinates are in Germany, true if they are outside germany.
    """
    log.add.info("validation user geo coordinates")
    try:
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&result_type=country&key={config.google_key}"
        ).json()["results"][0]["formatted_address"]
    except Exception as e:
        log.add.info(
            f"google geo valiadation failed, please check api key first, {str(e)}"
        )
        return True  # as something is defenitly wrong
    if response == "Germany":
        log.add.info(f"geo validation: ({lat}/{lng}) is a german location")
        return False
    else:
        print("hier unten")
        log.add.info(f"geo validation: ({lat}/{lng}) is not a german location")
        return True
