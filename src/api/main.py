from fastapi import FastAPI, APIRouter
from src.views.InsercaoView import insert_router
from src.views.CompetidorView import competidor_router
from src.views.ChaveamentoView import chaveamento_router
from src.views.JuradoView import jurado_router
from src.views.GraduacaoView import graduacao_router
from fastapi.middleware.cors import CORSMiddleware
from src.views.JogoView import jogo_router
from uvicorn import run

app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@router.get('/')
def initial():
    return 'Welcome here!'


app.include_router(prefix='/initial', router=router)
app.include_router(insert_router)
app.include_router(competidor_router)
app.include_router(chaveamento_router)
app.include_router(jurado_router)
app.include_router(graduacao_router)
app.include_router(jogo_router)
