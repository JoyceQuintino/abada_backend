from fastapi import FastAPI, APIRouter
from src.views.InsercaoView import insert_router

app = FastAPI()
router = APIRouter()

@router.get('/')
def initial():
    return 'Welcome here!'

app.include_router(prefix='/initial', router=router)
app.include_router(insert_router)