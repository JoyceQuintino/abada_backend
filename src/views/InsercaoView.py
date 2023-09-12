from fastapi import APIRouter

from src.services.InsertDataService import InsertDataService

insert_router = APIRouter(prefix='/insert')
assets_router = APIRouter(prefix='/assets')

@insert_router.get('/insert_data')
async def insert_data():
    try:
        await InsertDataService.inserting_data()
    except:
        pass
