from fastapi import APIRouter

from src.services import GraduacaoService

graduacao_router = APIRouter(prefix='/graduacao')
assets_router = APIRouter(prefix='/assets')

@graduacao_router.get('/insert_graduacao')
async def insert_graduacao():
    try:
        await GraduacaoService.insert_graduacao()
    except:
        pass

@graduacao_router.get('/get_all_graduacoes')
async def get_all():
    try:
        return await GraduacaoService.get_all_graduacoes()
    except:
        pass
