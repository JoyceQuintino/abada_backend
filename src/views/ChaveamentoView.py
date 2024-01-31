from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from src.services.ChaveamentoService import ChaveamentoService
from src.schemas.ChaveamentoSchema import ChaveamentoInput, ChaveamentoOutput

chaveamento_router = APIRouter(prefix='/chaveamento')
assets_router = APIRouter(prefix='/assets')

@chaveamento_router.get('/')
def get_root():
    return 'rota chaveamento'

@chaveamento_router.post('/categoria', response_model=ChaveamentoOutput)
async def chaveamento_jogos(payload: ChaveamentoInput, request: Request):
    return await ChaveamentoService.chaveamento_categoria(categoria=payload.model_dump()['categoria'])
