import pandas as pd

from src.models.models import Jogos, Pontuacoes
from src.database.db_connection import async_session
from sqlalchemy.future import select

class Pontuacao:
    @staticmethod
    async def insert_jogo(pontuacao: Pontuacoes):
        print('Cadastrando pontuacao...')
        async with async_session() as session:
            session.add(pontuacao)
            await session.commit()
