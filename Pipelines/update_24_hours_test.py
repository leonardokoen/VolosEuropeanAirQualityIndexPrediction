import logging
import logging.handlers
from Requests.AirQualityRequests import AirQualityRequests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status/get_24_hour_status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

if __name__ == "__main__":
    aqr = AirQualityRequests()
    try: 
        logger.info("[Initiate] Get 24 hour data.")
        data = aqr.get_24_hours_data()
        logger.info("[Success] Get 24 hour data.")
    except:
        logger.error("[Failed] Could not get 24 hour data")

