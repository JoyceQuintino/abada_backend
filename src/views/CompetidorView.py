from fastapi import APIRouter

from src.services.CompetidorService import CompeditorService

competidor_router = APIRouter(prefix='/competidor')
assets_router = APIRouter(prefix='/assets')

@competidor_router.get('/get_all')
async def get_all():
    try:
        return await CompeditorService().get_all_competitors()
    except:
        pass