from datetime import datetime, timedelta
from sqlalchemy import select
from src.models.models import Users
from fastapi.exceptions import HTTPException
from src.database.db_connection import async_session
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError
from decouple import config
from src.core.security import get_hash_password, verify_password
from typing import Optional
from uuid import UUID

class UserService:
    async def create_user(username, password):
        async with async_session() as session:
            try:
                session.add(
                    Users(
                        username=username,
                        password=get_hash_password(password)
                    ))
                await session.commit()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='User already exists'
                )

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[Users]:
        async with async_session() as session:
            result = await session.execute(select(Users).filter(Users.username == username))
            user_on_db = result.scalar()
            return user_on_db

    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[Users]:
        async with async_session() as session:
            result = await session.execute(select(Users).filter(Users.id == user_id))
            user_on_db = result.scalar()
            return user_on_db

    @staticmethod
    async def authenticate(username: str, password: str) -> Optional[Users]:
        user = await UserService.get_user_by_username(username=username)
        if not user:
            return None
        
        if not verify_password(
            password=password,
            hashed_password=user.password
        ):
            return None
        return user