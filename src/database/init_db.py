import pandas as pd
from asyncio import run
from src.database.db_connection import DBConnection
from src.models.models import Base

db_conn = DBConnection()
engine = db_conn.get_engine()

def insert_data() -> pd.DataFrame:
    data = pd.read_csv('database-abada.csv', sep=',')
    return data

async def create_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

async def insert_data():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

if __name__ == '__main__':
    #insert_data()
    run(create_database())