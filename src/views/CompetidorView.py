from fastapi import APIRouter

from src.services.CompetidorService import CompeditorService

competidor_route = APIRouter(prefix='/competidor')
assets_router = APIRouter(prefix='/assets')

@competidor_route.get('/get_all')
async def get_all():
    return await CompeditorService.get_all_competitors()
