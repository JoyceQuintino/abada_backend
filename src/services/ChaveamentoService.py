from sqlalchemy.future import select
from src.utils.util import round_robin, divide_players

from src.database.db_connection import async_session 
from src.models.models import Competidores


class ChaveamentoService:
    async def qualifiers_matches(self):
        async with async_session() as session:
            result = await session.execute(select(Competidores))
            players_divided = divide_players(result.scalars().all())
            matches = []
            for group in players_divided:
                matches.append(round_robin(group))
            return matches

