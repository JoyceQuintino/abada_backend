from os import getenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import URL

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class DBConnection:
    def __init__(self):
        self.__connection_string = URL.create(
                                    drivername=getenv('PG_DRIVERNAME'),
                                    username=getenv('PG_USER'),
                                    password=getenv('PG_PASS'), 
                                    host=getenv('PG_HOST'),
                                    port=getenv('PG_PORT'),
                                    database=getenv('PG_DB')
        )
        self.session = None

    def get_engine(self):
        """
        Return connection engine
        :param: None
        :return: engine connection database
        """
    
        engine = create_async_engine(self.__connection_string, echo=True)
        async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        return async_session