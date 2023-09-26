from fastapi import APIRouter

from src.services.JogoService import JogoService

jogo_router = APIRouter(prefix='/jogo')


@jogo_router.post('/fechar_jogo')
async def fechar_jogo(nota_jogador_1, nota_jogador_2, nota_jogo, jogo_id, jurado):
    return await JogoService().insert_jogo(nota=nota_jogo,
                                           pontuacao_1=nota_jogador_1,
                                           pontuacao_2=nota_jogador_2,
                                           jogo_id=jogo_id,
                                           jurado=jurado)


@jogo_router.get('/fechar_jogo')
async def fechar_jogo_get():
    return await JogoService().insert_jogo(nota="",
                                           jogo_valido=True,
                                           competidor_1=1,
                                           competidor_2=1,
                                           modalidade="",
                                           pontuacao_1=0,
                                           pontuacao_2=0,
                                           jogo_id=1)