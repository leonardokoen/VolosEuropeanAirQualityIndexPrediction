import hopsworks
import pandas as pd
class HopsworksRequests():
    def __init__(self) -> None:
        pass

    def connect(self) -> None:
        self.project = hopsworks.login()
        self.fs = self.project.get_feature_store()

    def close(self) -> None:
        pass

    def get_volos_breath_history(self) -> pd.DataFrame:
        volos_breath_history_fg =self.fs.get_feature_group("volos_breath_history", version=1)
        volos_breath_history_df = volos_breath_history_fg.read().sort_values(by='date').reset_index(drop=True)
        return volos_breath_history_df
