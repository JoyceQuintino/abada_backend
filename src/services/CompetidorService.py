from src.models.models import Competidor
from src.database.db_connection import DBConnection 
from sqlalchemy.future import select


class CompeditorService:
    async def get_all_competitors():
        async_session = DBConnection().get_engine()
        async with async_session() as session:
            result = await session.execute(select(Competidor))
            return result.scalars().all()
