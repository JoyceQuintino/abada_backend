import pandas as pd

from src.models.models import Jogos
from src.database.db_connection import async_session 

async def insert_jogo(nota, jogo_valido, competidor_1, competidor_2, modalidade, pontuacao) -> None:
    print('Cadastrando jogo...')
    async with async_session() as session:
        jogo = Jogos(
            nota=nota, 
            jogo_valido=jogo_valido, 
            id_competidor_1=competidor_1, 
            id_competidor_2=competidor_2, 
            id_modalidade=modalidade, 
            id_pontuacao=pontuacao)
        session.add(jogo)
        await session.commit()

