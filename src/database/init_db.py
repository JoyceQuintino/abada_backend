import asyncio

from src.database.db_connection import engine
from src.models.models import Base

async def create_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

asyncio.run(create_database())
