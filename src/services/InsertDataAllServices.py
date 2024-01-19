import pandas as pd

class InsertDataAllServices():

    def get_data_to_insert(file_name: str):
        data = pd.read_csv(file_name)
        data_df = pd.DataFrame(data)
        return data_df.to_dict()