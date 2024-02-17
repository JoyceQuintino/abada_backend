from datetime import datetime, timedelta
from src.models.models import Users
from fastapi.exceptions import HTTPException
from src.database.db_connection import async_session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserService:
    async def create_user(username, password):
        async with async_session() as session:
            try:
                session.add(
                    Users(
                        username=username,
                        password=crypt_context.hash(password)
                    ))
                await session.commit()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='User already exists'
                )
            
    async def user_login(user: Users, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )

        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expires_in) 

        payload = {
            'sub': user.username,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) 

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }
