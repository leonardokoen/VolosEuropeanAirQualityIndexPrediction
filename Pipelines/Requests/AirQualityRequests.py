from .decorators import validate_with_retry
from .FeatureExtractionFromResponses import FeatureExtractionFromResponses as fe
import requests
import pandas as pd

MAX_RETRIES = 15
DELAY = 1
EXCEPTION = Exception

class AirQualityRequests:
    def __init__(self,
                  url_current : str = "http://backend.greenyourair.org/volos_data",
                  url_history : str = "http://backend.greenyourair.org/volos_data_calendar"
                  ) -> None:
        self.url_current = url_current
        self.url_history = url_history
        self.fe = fe()

    def get_history_data(self) -> pd.DataFrame:
        response = self.__get_and_validate_status_code(url = self.url_history)
        history = self.fe.history_feature_extraction(response)
        return history

    def get_live_data(self) -> pd.DataFrame: 
        response = self.__get_and_validate_status_code(url = self.url_current)
        live_data = self.fe.live_data_feature_extraction(response)
        return live_data
    
    def get_24_hours_data(self) -> pd.DataFrame:
        response = self.__get_and_validate_status_code(url = self.url_current)
        data_24 = self.fe.data_24_hours_feature_extraction(response)
        return data_24
    
    @validate_with_retry(max_retries=MAX_RETRIES, delay=DELAY, exceptions=EXCEPTION)
    def __get_and_validate_status_code(self, url : str) -> requests.models.Response:
        response = requests.get(url = url)
        if response.status_code != 200:
            raise ValueError(f"Response Status Code: {response.status_code}")
        return response
    
    

    
