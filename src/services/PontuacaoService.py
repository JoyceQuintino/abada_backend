import pandas as pd

from src.models.models import Pontuacoes, Ranking
from src.schemas.PontuacaoSchema import PontuacaoInput, RankingInput
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
                jogo_valido = pontuacao.jogo_valido,
                id_user=pontuacao.id_user
            )
            session.add(new_pontuacao)
            await session.commit()

    @staticmethod
    async def create_ranking(nota: RankingInput):
        async with async_session() as session:
            new_ranking = Ranking(
                apelido=nota.apelido,
                numero=nota.numero,
                sexo=nota.sexo,
                categoria=nota.categoria,
                fase=nota.fase,
                id_competidor=nota.id_competidor,
                total_jogo=nota.total_jogo,
                total_competidor=nota.total_competidor,
                nota_total=nota.nota_total
            )
            session.add(new_ranking)
            await session.commit()