import pandas as pd

from src.models.models import Jogos, Pontuacoes, Competidores
from src.database.db_connection import async_session
from sqlalchemy.future import select
from sqlalchemy.orm import query
from sqlalchemy import update

class Pontuacao:
    @staticmethod
    async def insert_jogo(pontuacao: Pontuacoes):
        print('Cadastrando pontuacao...')
        async with async_session() as session:
            session.add(pontuacao)
            await session.commit()
            return

    @staticmethod
    async def update_pontuacao(pontuacao: Pontuacoes):
        async with async_session() as session:
            await session.execute(update(Jogos).filter(Jogos.id == pontuacao.id_jogo).values(nota=pontuacao.pontuacao_jogo))
            await session.execute(update(Competidores).filter(Competidores.id == pontuacao.pontuacao_competidor_1).values())
            await session.commit()
            # jogo = await session.execute(select(Jogos).where(Jogos.id == pontuacao.id_jogo))
            # competidor_1 = await session.execute(select(Competidores).where(Competidores.id == jogo.id_competidor_1))

# modalidade -> graduacao -> masc/fem

'''
    benguela: {
        graduacao: {
            jogos_masc = [],
            jogos_fem = []
        }
    },
    siriuna: {
        graduacao: {
            jogos_masc = [],
            jogos_fem = []
        }
    },
    sao_bento_grande: {
        graduacao: {
            jogos_masc = [],
            jogos_fem = []
        }
    }
'''
