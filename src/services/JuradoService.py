from src.models.models import Jurados
from src.database.db_connection import async_session 


class JuradoService:

    async def get_all_jurados(self):
        async with async_session() as session:
            result = await session.execute(select(Jurados))
            return result.scalars().all()
    
    @staticmethod
    async def insert_jurado(nome):
        print('Cadastrando jurado...')
        async with async_session() as session:
            jurado = Jurados(
                nome=nome
            )
            session.add(jurado)
            await session.commit()

