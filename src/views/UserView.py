from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from src.schemas import UserSchema
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.database.db_connection import async_session
from sqlalchemy.orm import Session
from typing import Any
from src.models.models import Users
from src.services.UserService import UserService
from src.core.security import create_access_token, create_refresh_token
from src.api.dependencies.user_deps import get_current_user
from src.schemas.UserSchema import UserDetail

user_router = APIRouter(prefix='/user', tags=['Usuário'])
assets_router = APIRouter(prefix='/assets')

@user_router.post('/create_user', response_model=UserSchema.StandardOutput, responses={400: {'model': UserSchema.ErrorOutput}})
async def create_user(user: UserSchema.UserInput):
    try:
        await UserService.create_user(
            username=user.username,
            password=user.password
        )
        return UserSchema.StandardOutput(message='Success')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.post('/login', response_model=UserSchema.TokenSchema )
async def login(data: UserSchema.UserInput) -> Any:
    user = await UserService.authenticate(
        username = data.username,
        password = data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid username or password!'
        )
    
    return {
        'access_token': create_access_token(user.id),
        'refresh_token': create_refresh_token(user.id)
    }
    
@user_router.post('/test-token', summary='Token testing', response_model=UserDetail)
async def test_token(user: Users = Depends(get_current_user)):
    return user