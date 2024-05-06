import random

import pandas as pd

from src.models.models import Competidores, Filiacoes, Graduacoes, Modalidades, Categorias
from src.database.db_connection import async_session 
from sqlalchemy.future import select
from sqlalchemy.orm import lazyload

def get_data_to_insert():
        competidores = pd.read_csv('dados_falsos.csv')
        data_frame = pd.DataFrame(competidores)
        return data_frame


def get_data_categoria():
    categorias = pd.read_csv('categorias.csv')
    data_frame = pd.DataFrame(categorias)
    return data_frame


class InsertDataService:

    """ Função para adicionar categorias no banco de dados """
    @staticmethod
    async def insert_categorias():
        data = get_data_categoria()
        categorias = []
        async with async_session() as session:
            for row in data.itertuples():
                categorias.append(Categorias(nome=row.nome))
            session.add_all(categorias)
            await session.commit()

    """ Função para adicionar modalidades dentro do banco """
    @staticmethod
    async def insert_modalidade():
        async with async_session() as session:
            modalidades=["siriuna", "benguela", "são bento grande"]
            modalidades_to_save = []
            for modalidade in modalidades:
                modalidade_save = Modalidades(nome=modalidade)
                modalidades_to_save.append(modalidade_save)
            session.add_all(modalidades_to_save)
            await session.commit()

    """ Inserir dados de todos os competidores na tabela """
    @staticmethod
    async def inserting_data():
        data = get_data_to_insert()
        async with async_session() as session:
            result = await session.execute(select(Graduacoes).options(lazyload(Graduacoes.categoria)))
            graduacoes = []
            competidores = []
            for row in result:
                for item in row:
                    if item not in graduacoes:
                        graduacoes.append(item)
            for graduacao in graduacoes:
                for row in data.itertuples():
                    if row.graduacao.lower() == graduacao.nome:
                        competidor = Competidores(
                            nome=row.nome,
                            apelido=row.apelido,
                            numero=row.numero,
                            cidade=row.cidade,
                            estado=row.estado,
                            sexo=row.sexo,
                            id_graduacao=graduacao.id
                        )
                        competidores.append(competidor)
            # print(competidores)
            session.add_all(competidores)
            await session.commit()
            