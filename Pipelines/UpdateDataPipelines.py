from Requests.AirQualityRequests import AirQualityRequests
from Requests.HopsworksRequests import HopsworksRequests

class UpdatePipelines():
    def __init__(self) -> None:
        self.aqr = AirQualityRequests()
        self.hr = HopsworksRequests()

    def update_24_hour_data(self):
        self.hr.connect()
    
    def update_history(self):
        self.hr.connect()
        
