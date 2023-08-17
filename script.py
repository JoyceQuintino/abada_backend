import pandas as pd

competidores = pd.read_csv('database-abada.csv')
data_frame = pd.DataFrame(competidores)
for row in data_frame.itertuples():
    print(row.graduacao)