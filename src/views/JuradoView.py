from fastapi import APIRouter
from src.services import JuradoService
from src.schemas import JuradoSchema

jurado_router = APIRouter(prefix='/jurado')
assets_router = APIRouter(prefix='/assets')

@jurado_router.post('/jurado_create', response_model=JuradoSchema.StandardOutput)
async def jurado_create(jurado_input: JuradoSchema.JuradoCreateInput):
    try:
        await JuradoService.insert_jurado(nome=jurado_input.nome)
        return JuradoSchema.StandardOutput(message='OK')
    except:
        pass

