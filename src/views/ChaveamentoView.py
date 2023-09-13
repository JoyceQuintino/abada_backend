from fastapi import APIRouter
from starlette.responses import RedirectResponse
from src.services.ChaveamentoService import ChaveamentoService

chaveamento_route = APIRouter(prefix='/chaveamento')
assets_router = APIRouter(prefix='/assets')


@chaveamento_route.get('/')
def get_root():
    return 'rota chaveamento'

@chaveamento_route.get('/qualifiers')
async def get_qualifiers():
    return await ChaveamentoService().qualifiers()

@chaveamento_route.get('/get_qualifiers')
async def get_qualifiers_matches():
    await ChaveamentoService().qualifiers_matches()
    return RedirectResponse(url='/chaveamento/qualifiers')

@chaveamento_route.get('/get_semifinals')
async def get_semifinals():
    return await ChaveamentoService().semifinals()
