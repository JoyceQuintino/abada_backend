from fastapi import APIRouter
from src.services.ChaveamentoService import ChaveamentoService

chaveamento_router = APIRouter(prefix='/chaveamento')
assets_router = APIRouter(prefix='/assets')

@chaveamento_router.get('/')
def get_root():
    return 'rota chaveamento'

@chaveamento_router.get('/get_qualifiers')
async def get_qualifiers_matches():
    return await ChaveamentoService().qualifiers_matches()
