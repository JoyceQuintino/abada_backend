from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from fastapi import Depends, HTTPException, status
from src.models.models import Users
from jose import jwt
from src.schemas.AuthSchema import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from src.services.UserService import UserService

ALGORITHM = "HS256"

oauth_reusable = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    scheme_name='JWT'
)

async def get_current_user(token: str = Depends(oauth_reusable)) -> Users:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            ALGORITHM
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expired',
                headers={'WWW-Authenticate': 'Bearer'}
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token validation error',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user = await UserService.get_user_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Could not find the user',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return user