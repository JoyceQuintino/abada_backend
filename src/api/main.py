from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

@router.get('/')
def initial():
    return 'Welcome here!'

app.include_router(prefix='/initial', router=router)