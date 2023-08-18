import pandas as pd

competidores = pd.read_csv('database-abada.csv')
data_frame = pd.DataFrame(competidores)
for row in data_frame.itertuples():
    ''' Criar os objetos usando o cada linha e inserir diretamente no banco de dados '''
    print(row.graduacao)