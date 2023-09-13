import pandas as pd

from src.models.models import Competidor, Filiacao, Graduacao, CategoriaEnum, Jurado
from src.database.db_connection import async_session 

def get_data_to_insert():
        competidores = pd.read_csv('database-abada.csv')
        data_frame = pd.DataFrame(competidores)
        return data_frame

class InsertDataService:
    async def inserting_data():
        data = get_data_to_insert()
        async with async_session() as session:
            for row in data.itertuples():
                competidor = Competidor(
                    nome=row.nome,
                    apelido=row.apelido,
                    cidade=row.cidade,
                    estado=row.estado
                )
                session.add(competidor)
                await session.commit()
            