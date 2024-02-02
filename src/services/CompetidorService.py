from src.models.models import Competidores
from src.database.db_connection import async_session
from sqlalchemy.future import select


class CompeditorService:
    async def get_all_competitors(self):
        async with async_session() as session:
            result = await session.execute(select(Competidores))
            competidores = result.scalars().all()
            nomes = []
            for competidor in competidores:
                nomes.append(competidor.nome)
            return competidores