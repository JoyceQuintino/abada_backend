import pandas as pd

from src.models.models import Pontuacoes
from src.schemas.PontuacaoSchema import PontuacaoInput
from src.database.db_connection import async_session
from sqlalchemy.future import select
from sqlalchemy.orm import query
from sqlalchemy import update

class PontuacaoService:

    @staticmethod
    async def create_pontuacao(pontuacao: PontuacaoInput):
        async with async_session() as session:
            new_pontuacao = Pontuacoes(
                pontuacao_competidor_1=pontuacao.pontuacao_competidor_1,
                pontuacao_competidor_2=pontuacao.pontuacao_competidor_2,
                pontuacao_jogo=pontuacao.pontuacao_jogo,
                id_jogo=pontuacao.id_jogo,
                id_user=pontuacao.id_user
            )
            session.add(new_pontuacao)
            await session.commit()