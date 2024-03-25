from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
from src.services.ChaveamentoService import ChaveamentoService
from src.schemas.ChaveamentoSchema import ChaveamentoInput

tokens_validos = ['08f57f2c-ac47-4e52-8098-f3fce671b0f0']

chaveamento_router = APIRouter(prefix='/chaveamento', tags=['Chaveamento'])
assets_router = APIRouter(prefix='/assets')

@chaveamento_router.post('/categoria_teste')
async def chaveamento_jogos_teste(payload: ChaveamentoInput, request: Request):
    return await ChaveamentoService.chaveamento_categoria_teste(categoria=payload.model_dump()['categoria'])

@chaveamento_router.get('/get_all_chaveamento', summary="Obter todos os jogadores")
async def get_all_chaveamento(request: Request):
    """
    Obtém todos os jogadores.

    Returns:
        List[dict]: Lista de dicionários contendo os dados dos jogadores.
    """
    return await ChaveamentoService().get_all_chaveamento()
    

@chaveamento_router.post('/categoria', summary="Gerar chaveamento de jogos para uma categoria")
async def chaveamento_jogos(payload: ChaveamentoInput, request: Request):
    """
    Gera chaveamento de jogos para uma categoria.

    Args:
        payload (ChaveamentoInput): Objeto contendo os dados da categoria.

    Returns:
        dict: Dicionário contendo o chaveamento da categoria.
    """

    if payload.token not in tokens_validos:
        raise HTTPException(status_code=403, detail="Token inválido")

    if 'categoria' in payload.model_dump():
        categorias = payload.model_dump()['categoria']
        return await ChaveamentoService().chaveamento_categoria(categorias=categorias)
    else:
        raise HTTPException(status_code=400, detail="Nenhuma categoria fornecida no payload")