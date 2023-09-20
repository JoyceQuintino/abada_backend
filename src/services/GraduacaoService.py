import pandas as pd

from src.services.InsertDataAllServices import InsertDataAllServices
from src.models.models import Graduacoes
from src.database.db_connection import async_session
from sqlalchemy.future import select

PATH_NAME = 'graduacoes_data.csv'

def get_data_to_insert():
        data = pd.read_csv('graduacoes_data.csv')
        data_df = pd.DataFrame(data)
        return data_df

class GraduacaoService:
    async def insert_graduacao():
        data = InsertDataAllServices.get_data_to_insert('data/graduacoes_data.csv')
        async with async_session() as session:
            for row in data.itertuples():
                graduacao = Graduacoes(
                    nome=row.nome
                )
                session.add(graduacao)
                await session.commit()
            
    async def get_all_graduacoes(self):
        async with async_session() as session:
            result = await session.execute(select(Graduacoes))
            return result.scalars().all()