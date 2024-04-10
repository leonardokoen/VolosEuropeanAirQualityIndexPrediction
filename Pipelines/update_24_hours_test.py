import logging
import logging.handlers
from Requests.AirQualityRequests import AirQualityRequests
from Requests.HopsworksRequests import HopsworksRequests
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status/get_24_hour_status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

if __name__ == "__main__":
    aqr = AirQualityRequests()
    hr = HopsworksRequests()

    try: 
        logger.info("[Initiate] Get last 24 hour data from Green Your Air Backend Call.")
        data = aqr.get_24_hours_data()
        logger.info("[Success] Get last 24 hour data from Green Your Air Backend Call.")
    except:
        logger.error("[Failed] last 24 hour data from Green Your Air Backend Call.")
        raise Exception
    
    try:
        logger.info("[Initiate] Connect to hopsworks feature store.")
        hr.connect()
        logger.info("[Success] Connect to hopsworks feature store.")
    except:
        logger.error("[Failed] Could not connect to hopsworks feature store.")
        raise Exception



