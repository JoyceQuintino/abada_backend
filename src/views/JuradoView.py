from fastapi import APIRouter, HTTPException
from src.services import JuradoService
from src.schemas import JuradoSchema

jurado_router = APIRouter(prefix='/jurado')
assets_router = APIRouter(prefix='/assets')

@jurado_router.post('/insert_jurado', description='My description', response_model=JuradoSchema.StandardOutput, responses={400: {'model': JuradoSchema.ErrorOutput}})
async def insert_jurado(jurado_input: JuradoSchema.JuradoInput):
    try:
        await JuradoService.insert_jurado(nome=jurado_input.nome)
        return JuradoSchema.StandardOutput(message='OK')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@jurado_router.get('/get_all_jurados', response_model=JuradoSchema.StandardOutput)
async def get_all_jurados():
    try:
        await JuradoService.get_all_jurados()
        return JuradoSchema.StandardOutput(message='Todos os jurados cadastrados')
    except Exception as error:
        raise HTTPException(400, detail=str(errors))

