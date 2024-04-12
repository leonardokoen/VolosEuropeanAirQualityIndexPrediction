import logging
import logging.handlers
from Requests.AirQualityRequests import AirQualityRequests
from Requests.HopsworksRequests import HopsworksRequests
import pickle as pkl

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info(20*"-" + "Pipeline update_24_hours_pipeline Initiated" + 20*"-")
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
    index_filepath = "Pipelines/update_24_hours_index.pkl"

    #Get last index
    try:
        logger.info("[Initiate] Get the last index from pickle file.")
        with open(index_filepath, "rb") as file:
            index = pkl.load(file)
        logger.info(f"[Success] Index retrieved successfully with value {index}.")
    except Exception as e:
        logger.error(f"[Failed] Couldn't retrieve index from pickle file: {e}")
        raise

    #Get data from the greenyourair api
    try: 
        logger.info("[Initiate] Get last 24 hour data from Green Your Air Backend Call.")
        data = aqr.get_24_hours_data()
        data.at[0, 'index'] = index + 1
        logger.info("[Success] Get last 24 hour data from Green Your Air Backend Call.")
    except Exception as e:
        logger.error(f"[Failed] Couldn't fetch last 24 hour data from Green Your Air Backend Call: {e}")
        raise

    #Connect to Hopsworks Feature Store
    try:
        logger.info("[Initiate] Connect to hopsworks feature store.")
        hr.connect()
        feature_store = hr.get_fs()
        logger.info("[Success] Connect to hopsworks feature store.")
    except Exception as e:
        logger.error(f"[Failed] Could not connect to hopsworks feature store: {e}")
        raise

    #Get Hopsworks Feature Group
    try: 
        logger.info(f"[Initiate] Get hopsworks feature group - name: volos_breath_daily_tracker , version = {1}")
        feature_group = feature_store.get_feature_group(name="volos_breath_daily_tracker", version = 1)
        logger.info(f"[Success] Get hopsworks feature group - name: volos_breath_daily_tracker , version = {1}" )
    except Exception as e:
        logger.error(f"[Failed] Could not get feature group: {e}")

    #Insert data to Feature Group
    try:
        logger.info("[Initiate] Inserting data to feature group.")
        feature_group.insert(data, overwrite=False, storage="online")
        logger.info("[Success] Inserting data to feature group.")
    except Exception as e:
        logger.error(f"[Failed] Could not insert data to feature group: {e}")

    #Update the index in the pickle file.
    try:
        logger.info(f"[Initiate] Change the index in pickle file to value: {index + 1}.")
        with open(index_filepath, "wb") as file:
            #clear existing file
            file.write(b"")
            #dump new index
            pkl.dump(index+1, file)
        logger.info(f"[Success] Index changed successfully to value: {index + 1}.")
    except Exception as e:
        logger.error(f"[Failed] Couldn't retrieve index from pickle file: {e}")
        raise




