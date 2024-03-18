from fastapi import APIRouter

from src.services.InsertDataService import InsertDataService
from src.services.GraduacaoService import GraduacaoService
from src.services.CompetidorService import CompeditorService

insert_router = APIRouter(prefix='/insert', tags=['Inserções de Dados'])
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

@insert_router.get('/insert_all_data')
async def insert_all_data():
    await InsertDataService.insert_categorias()
    await InsertDataService.insert_modalidade()
    await GraduacaoService.insert_graduacao()
    await InsertDataService.inserting_data()