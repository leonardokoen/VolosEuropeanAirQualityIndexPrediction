import pandas as pd
import numpy as np
from .Utilities.utilities import calculate_eaqi
import requests
from datetime import datetime
import pytz

class FeatureExtractionFromResponses():
    def __init__(self) -> None:
        pass
    
    def history_feature_extraction(self, response : requests.models.Response):
        history_data = response.json()['data']
        history_data = pd.DataFrame(history_data)
        history_data = history_data.drop(['exists'], axis = 1)
        history_data['date'] = pd.to_datetime(history_data['date'])
        history_data['value'] = history_data['value'].replace('', '0')
        history_data['value'] = history_data['value'].astype(float)
        history_data['value'] = history_data['value'].replace(0.0, np.nan)
        history_data['value'] = history_data['value'].fillna(history_data['value'].mean())
        history_data['index'] = history_data['value'].apply(calculate_eaqi)
        history_data = history_data.rename(columns={'index':'eaqi_index'})
        history_data = history_data.reset_index()
        return history_data
    
    def live_data_feature_extraction(self, response : requests.models.Response):
        
        live_data = response.json()['live']
        live_data['live_value'] = [float(live_data['live_value'])]
        live_data['live_time'] = [live_data['live_time']]
        
        greece_tz = pytz.timezone('Europe/Athens')
        current_datetime = datetime.now(greece_tz)
        current_datetime = pd.to_datetime(current_datetime)

        live_data = pd.DataFrame(live_data)
        live_data = live_data.drop(['live_time'], axis = 1)
        live_data = live_data.rename(columns={'live_value':'value'})
        live_data['date'] = current_datetime.date()
        live_data['time'] = current_datetime.strftime('%H:%M:%S')
        live_data['index'] = live_data['value'].apply(calculate_eaqi)
        live_data = live_data[['date', 'time', 'value', 'index']]
        return live_data
    
    def data_24_hours_feature_extraction(self, response : requests.models.Response) -> pd.DataFrame:
        greece_tz = pytz.timezone('Europe/Athens')
        current_datetime = datetime.now(greece_tz)

        data_24 = response.json()['data']
        data_24 = pd.DataFrame(data_24)
        data_24 = data_24.rename(columns={0:'value'})
        data_24['value'] = data_24['value'].astype(float)
        data_average = pd.DataFrame(columns=['index', 'date', 'value'])
        data_average.loc[len(data_average.index)] = [0, current_datetime.date(), data_24['value'].mean()]
        data_average['index'] = data_average['index'].astype('Int64')
         
        data_average['eaqi_index'] = data_average['value'].apply(calculate_eaqi)
        return data_average