from fastapi import FastAPI, APIRouter
from src.views.InsercaoView import insert_router
from src.views.CompetidorView import competidor_router
from src.views.ChaveamentoView import chaveamento_router
from src.views.JuradoView import jurado_router
from src.views.GraduacaoView import graduacao_router

app = FastAPI()
router = APIRouter()

@router.get('/')
def initial():
    return 'Welcome here!'

app.include_router(prefix='/initial', router=router)
app.include_router(insert_router)
app.include_router(competidor_router)
app.include_router(chaveamento_router)
app.include_router(jurado_router)
app.include_router(graduacao_router)
