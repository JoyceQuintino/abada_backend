from fastapi import APIRouter
from src.services.JuradoService import JuradoService
from src.schemas import JuradoSchema

jurado_router = APIRouter(prefix='/jurado')
assets_router = APIRouter(prefix='/assets')

@jurado_router.post('/insert_jurado', response_model=JuradoSchema.StandardOutput)
async def jurado_create(jurado_input: JuradoSchema.JuradoInput):
    try:
        await JuradoService.insert_jurado(nome=jurado_input.nome)
        return JuradoSchema.StandardOutput(message='OK')
    except:
        pass

@jurado_router.get('/get_all_jurados')
async def get_all_jurados():
    return await JuradoService().get_all_jurados()