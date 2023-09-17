from fastapi import APIRouter
from src.services import JuradoService
from src.schemas import JuradoSchema

jurado_router = APIRouter(prefix='/insert')
assets_router = APIRouter(prefix='/assets')

@jurado_router.post('/insert_jurado', response_model=JuradoSchema.StandardOutput)
async def jurado_create(jurado_input: JuradoSchema.JuradoInput):
    try:
        await JuradoService.insert_jurado(nome=jurado_input.nome)
        return JuradoSchema.StandardOutput(message='OK')
    except:
        pass

