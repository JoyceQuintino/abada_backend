import pandas as pd

from src.models.models import Jogos, Pontuacoes
from src.database.db_connection import async_session
from sqlalchemy.future import select


class JogoService:
    async def insert_jogo(self,
                          nota,
                          pontuacao_1,
                          pontuacao_2,
                          jogo_id,
                          jurado):
        print('Cadastrando pontuacao...')
        async with async_session() as session:
            result = await session.execute(select(Jogos).where(Jogos.id == jogo_id))
            jogo = await result.scalars().all()
            pontuacao = Pontuacoes(pontuacao_competidor_1=pontuacao_1,
                                   pontuacao_competidor_2=pontuacao_2,
                                   pontuacao_jogo=nota,
                                   id_jurado=jurado,
                                   id_jogo=jogo.id)
            await session.add(pontuacao)
            session.commit()

