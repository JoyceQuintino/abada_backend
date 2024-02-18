from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from src.schemas import UserSchema
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.database.db_connection import async_session
from sqlalchemy.orm import Session
from typing import Any
from src.services.UserService import UserService
from src.core.security import create_access_token, create_refresh_token

user_router = APIRouter(prefix='/user')
assets_router = APIRouter(prefix='/assets')

@user_router.post('/create_user', response_model=UserSchema.StandardOutput, responses={400: {'model': UserSchema.ErrorOutput}})
async def create_user(user: UserSchema.UserCreateInput):
    try:
        await UserService.create_user(
            username=user.username,
            password=user.password
        )
        return UserSchema.StandardOutput(message='Success')
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@user_router.post('/login', responses={400: {'model': UserSchema.ErrorOutput}})
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(
        username = data.username,
        password = data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid username or password!'
        )
    # Criar access_token
    return {
        'access_token': create_access_token(user.id),
        'refresh_token': create_refresh_token(user.id)
    }
    