from fastapi import APIRouter

from src.services.CategoriaService import CategoriaService

categoria_router = APIRouter(prefix='/categoria')
assets_router = APIRouter(prefix='/assets')

@categoria_router.get('/get_all_categorias')
async def get_all_categorias():
    return await CategoriaService().get_all_categorias()