from fastapi import FastAPI, APIRouter
from src.views.InsercaoView import insert_router
from src.views.CompetidorView import competidor_route
from src.views.ChaveamentoView import chaveamento_route

app = FastAPI()
router = APIRouter()


@router.get('/')
def initial():
    return 'Welcome here!'


app.include_router(prefix='/initial', router=router)
app.include_router(insert_router)
app.include_router(competidor_route)
app.include_router(chaveamento_route)
