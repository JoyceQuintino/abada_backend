import pandas as pd

from src.models.models import Competidor, Filiacao, Graduacao, CategoriaEnum, Jurado
from src.database.db_connection import DBConnection 

def get_data_to_insert():
        competidores = pd.read_csv('database-abada.csv')
        data_frame = pd.DataFrame(competidores)
        return data_frame

class InsertDataService:
    async def inserting_data():
        data = get_data_to_insert()
        async_session = DBConnection().get_engine()
        async with async_session() as session:
            for row in data.itertuples():
                if row.graduacao in CategoriaEnum.laranja_laranja_azul.__str__():
                    graduacao = Graduacao(nome=row.graduacao, categoria=CategoriaEnum.laranja_laranja_azul)
                    session.add(graduacao)
                elif row.graduacao in CategoriaEnum.azul_azul_verde.__str__():
                    graduacao = Graduacao(nome=row.graduacao, categoria=CategoriaEnum.azul_azul_verde)
                    session.add(graduacao)
                elif row.graduacao in CategoriaEnum.verde_verde_roxa.__str__():
                    graduacao = Graduacao(nome=row.graduacao, categoria=CategoriaEnum.verde_verde_roxa)
                    session.add(graduacao)
                elif row.graduacao in CategoriaEnum.roxa_roxa_marrom.__str__():
                    graduacao = Graduacao(nome=row.graduacao, categoria=CategoriaEnum.roxa_roxa_marrom)
                    session.add(graduacao)
                elif row.graduacao in CategoriaEnum.marrom_marrom_vermelha.__str__():
                    graduacao = Graduacao(nome=row.graduacao, categoria=CategoriaEnum.marrom_marrom_vermelha)
                    session.add(graduacao)
                filiacao = Filiacao(nome_professor=row.filiacao, graduacao_professor='teste')
                competidor = Competidor(
                    nome=row.nome,
                    apelido=row.apelido,
                    nome_estado=f'{row.cidade}-{row.estado}')
                session.add(filiacao)
                session.add(competidor)
                await session.commit()
            