from sqlalchemy import desc
from sqlalchemy.future import select
from src.utils.util import round_robin, divide_players

from src.database.db_connection import async_session 
from src.models.models import Competidor, Jogo


class ChaveamentoService:
    async def qualifiers_matches(self):
        async with async_session() as session:
            result = await session.execute(select(Competidor))
            players_divided = divide_players(result.scalars().all())
            matches = []
            for group in players_divided:
                match_groups = round_robin(group)
                matches.append(match_groups[0])
                matches.append(match_groups[1])
            for match in matches:
                result = await session.execute(select(Jogo))
                jogos = result.scalars().all()
                print(jogos)
                if match[0] not in jogos:
                    session.add_all([match[0], match[1]])
                    await session.commit()
            return matches



    async def qualifiers(self):
        async_session = DBConnection().get_engine()
        async with async_session() as session:
            result = await session.execute(select(Jogo))
            jogos_competidores = []
            for jogo in result.scalars().all():
                competidor_1 = await session.execute(select(Competidor).filter(jogo.id_competidor_1 == Competidor.id))
                competidor_2 = await session.execute(select(Competidor).filter(jogo.id_competidor_2 == Competidor.id))
                jogos_competidores.append([jogo,
                                       competidor_1.scalars().all(),
                                       competidor_2.scalars().all()])
            return jogos_competidores


    async def semifinals(self):
        async_session = DBConnection().get_engine()
        async with async_session() as session:
            result = await session.execute(select(Competidor).order_by(desc(Competidor.nome)).limit(8))
            return result.scalars().all()

    async def final(self):
        pass
