import math
from datetime import datetime
from epi.prediction import predictor
from epi.forcast import climate
from epi.forcast import weather
from epi.prediction import evaluator
from epi.helpers import common
from epi import logger as log


def run(lat, lng, start, end, dur, test):
    """
    Selects the appropriate prediction mehtod.

        Parameters:
        ----------

            lat : float
                Lattitude.

            lng : float
                Longitude. 

            start : str
                Earliest start-date.

            end : str
                Latest end-date.

            dur : int
                Duration in minutes.

            test : bool
                True if the request is for testing purposes.

        Returns:
        ----------

            result : str
                Prediction result.
            
            if test==True

                prediction : str

                prediction_direct_hit : bool
                    If prediction matches the real ideal time.

                randome_direct_hit : boole
                    If randome selction matches the real ideal time.

    """
    days_in_future = (common.str_to_datetime(start) - datetime.now()).days
    if test == "test":
        # distinction relevant to not exceed the max. weather api calls
        prediction = predictor.ar_prediction(start, end, dur)
        target = evaluator.run(start, end, dur)[0]
        randome_direct_hit = evaluator.run(start, end, dur)[1]
        prediction_direct_hit = prediction == target
        randome_direct_hit = randome_direct_hit == target
        result = prediction, prediction_direct_hit, randome_direct_hit
        log.add.info("returned evaluation results")
        return result
    if days_in_future < 30:
        if days_in_future < 4:
            result = weather.get_best_start(lat, lng, start, end, dur)
            log.add.info(f"returned weather forcast-based suggestion ({result})")
            return result
        else:
            if (math.ceil(dur / 60)) < 24:
                result = predictor.ar_prediction(start, end, dur)
                log.add.info(f"returned machine learning-based suggestion ({result})")
                return result
            else:
                result = climate.get_best_start(lat, lng, start, end, dur)
                log.add.info(f"returned climate forcast-based suggestion ({result})")
                return result
    else:
        result = predictor.ar_prediction(start, end, dur)
        log.add.info(f"returned machine learning-based suggestion ({result})")
        return result
