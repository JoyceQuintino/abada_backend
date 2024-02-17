from fastapi import APIRouter
from src.models.models import Pontuacoes
from src.services.PontuacaoService import Pontuacao
from fastapi import status
# from src.schemas.PontuacaoSchema import PontuacaoRequest

pontuacao_router = APIRouter(prefix='/pontuacao')


@pontuacao_router.post('/insert_pontuacao')
async def insert_pontuacao(request: dict):
    pontuacao_competidor_1 = float(request["pontuacao_competidor_1"])
    pontuacao_competidor_2 = float(request["pontuacao_competidor_2"])
    pontuacao_jogo = float(request["pontuacao_jogo"])
    jogo = request["id_jogo"]
    jurado = request["id_jurado"]
    pontuacao = Pontuacoes(pontuacao_competidor_1=pontuacao_competidor_1,
                           pontuacao_competidor_2=pontuacao_competidor_2,
                           pontuacao_jogo=pontuacao_jogo,
                           id_jurado=jurado,
                           id_jogo=jogo)
    # return pontuacao
    # return await Pontuacao.update_pontuacao(pontuacao)
    return await Pontuacao().insert_jogo(pontuacao)

# pontuacao_competidor_1 = Column('pontuacao_competidor_1', Float, nullable=False)
#     pontuacao_competidor_2 = Column('pontuacao_competidor_2', Float, nullable=False)
#     pontuacao_jogo = Column('pontuacao_jogo', Float, nullable=False)
#     id_jurado = Column('id_jurado', UUID(), ForeignKey('Jurados.id', ondelete='CASCADE'))
#     id_jogo = Column('id_jogo', UUID(), ForeignKey('Jogos.id', ondelete='CASCADE'))


@pontuacao_router.get('/get_pontuacao')
async def get_pontuacao():
    return await Pontuacao().insert_jogo(nota="",
                                           jogo_valido=True,
                                           competidor_1=1,
                                           competidor_2=1,
                                           modalidade="",
                                           pontuacao_1=0,
                                           pontuacao_2=0,
                                           jogo_id=1)