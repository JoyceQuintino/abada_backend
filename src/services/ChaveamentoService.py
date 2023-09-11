from sqlalchemy.future import select
from src.Utils.Util import round_robin, divide_players

from src.database.db_connection import DBConnection
from src.models.models import Competidor


class ChaveamentoService:
    async def qualifiers_matches(self):
        async_session = DBConnection().get_engine()
        async with async_session() as session:
            result = await session.execute(select(Competidor))
            players_divided = divide_players(result.scalars().all())
            matches = []
            for group in players_divided:
                matches.append(round_robin(group))
            return matches

