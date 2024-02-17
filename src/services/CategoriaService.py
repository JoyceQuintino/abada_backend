from src.models.models import Categorias
from src.database.db_connection import async_session
from sqlalchemy.future import select

class CategoriaService:
    async def get_all_categorias(self):
        async with async_session() as session:
            result = await session.execute(select(Categorias))
            return result.scalars().all()