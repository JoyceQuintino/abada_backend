from fastapi import APIRouter
from src.services.ChaveamentoService import ChaveamentoService

chaveamento_route = APIRouter(prefix='/chaveamento')
assets_router = APIRouter(prefix='/assets')


@chaveamento_route.get('/')
def get_root():
    return 'rota chaveamento'


@chaveamento_route.get('/get_qualifiers')
async def get_qualifiers_matches():
    return await ChaveamentoService().qualifiers_matches()
