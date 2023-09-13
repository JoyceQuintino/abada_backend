from fastapi import APIRouter
from starlette.responses import RedirectResponse
from src.services.ChaveamentoService import ChaveamentoService

chaveamento_router = APIRouter(prefix='/chaveamento')
assets_router = APIRouter(prefix='/assets')

@chaveamento_router.get('/')
def get_root():
    return 'rota chaveamento'

@chaveamento_router.get('/qualifiers')
async def get_qualifiers():
    return await ChaveamentoService().qualifiers()

@chaveamento_router.get('/get_qualifiers')
async def get_qualifiers_matches():
    await ChaveamentoService().qualifiers_matches()
    return RedirectResponse(url='/chaveamento/qualifiers')

@chaveamento_router.get('/get_semifinals')
async def get_semifinals():
    return await ChaveamentoService().semifinals()
