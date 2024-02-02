import pandas as pd

from src.services.InsertDataAllServices import InsertDataAllServices
from src.models.models import Graduacoes, Categorias
from src.database.db_connection import async_session
from sqlalchemy.future import select

PATH_NAME = 'graduacoes_data.csv'

def get_data_to_insert():
        data = pd.read_csv('graduacoes_data.csv')
        data_df = pd.DataFrame(data)
        return data_df

def to_lowercase(element: str):
    return element.lower()

class GraduacaoService:
    async def insert_graduacao():
        data = InsertDataAllServices.get_data_to_insert('data/graduacoes_data.csv') # recebo o dictionary contendo os valores das graduacoes
        graduacoes = list(map(to_lowercase, data.get('nome').values()))
        async with async_session() as session:
            graduacoes_to_save = []
            result = await session.execute(select(Categorias))
            categorias = result.scalars().all()
            for graduacao in graduacoes:
                for categoria in categorias:
                    if categoria.nome.startswith(graduacao.split('-')[0]):
                        graduacao_to_save = Graduacoes(nome=graduacao, id_categoria=categoria.id)
                        graduacoes_to_save.append(graduacao_to_save)
            session.add_all(graduacoes_to_save)
            await session.commit()
           
            
    async def get_all_graduacoes(self):
        async with async_session() as session:
            result = await session.execute(select(Graduacoes))
            return result.scalars().all()