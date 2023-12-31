from fastapi import APIRouter

from src.services.InsertDataService import InsertDataService

insert_router = APIRouter(prefix='/insert')
assets_router = APIRouter(prefix='/assets')


@insert_router.get('/insert_data')
async def insert_data():
    return await InsertDataService.inserting_data()


@insert_router.get('/insert_modalidade')
async def insert_modalidade():
    return await InsertDataService().insert_modalidade()


@insert_router.get('/insert_categorias')
async def insert_categorias():
    return await InsertDataService.insert_categorias()
