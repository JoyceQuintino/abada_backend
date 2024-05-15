from fastapi import FastAPI, APIRouter
from src.views.InsercaoView import insert_router
from src.views.CompetidorView import competidor_router
from src.views.ChaveamentoView import chaveamento_router
from src.views.GraduacaoView import graduacao_router
from src.views.CategoriaView import categoria_router
from fastapi.middleware.cors import CORSMiddleware
from src.views.PontuacaoView import pontuacao_router
from src.views.UserView import user_router
from uvicorn import run
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME
)
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
app.include_router(graduacao_router)
app.include_router(pontuacao_router)
app.include_router(categoria_router)
app.include_router(user_router)
