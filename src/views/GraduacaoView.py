from fastapi import APIRouter

from src.services.GraduacaoService import GraduacaoService

graduacao_router = APIRouter(prefix='/graduacao')
assets_router = APIRouter(prefix='/assets')

@graduacao_router.get('/insert_graduacao')
async def insert_graduacao():
    return await GraduacaoService.insert_graduacao()

@graduacao_router.get('/get_all_graduacoes')
async def get_all():
    try:
        return await GraduacaoService.get_all_graduacoes()
    except:
        pass
