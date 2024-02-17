from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from src.schemas import UserSchema
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.database.db_connection import async_session
from sqlalchemy.orm import Session
from src.services.UserService import UserService

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

@user_router.post('/login', response_model=UserSchema.StandardOutput, responses={400: {'model': UserSchema.ErrorOutput}})
async def user_login(
    request_form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(async_session),
):
    try:

        user = UserService.user_login(
            username = request_form_user.username,
            password = request_form_user.password
        )

        auth_data = user.user_login(user=user)
        return JSONResponse(
            content=auth_data,
            status_code=status.HTTP_200_OK
        )
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    