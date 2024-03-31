import re
from pydantic import BaseModel, validator, Field
from typing import Optional
from uuid import UUID

class UserInput(BaseModel):
    username: str = Field(..., min_length=5, max_length=50, description='Username')
    password: str = Field(..., min_length=5, max_length=20, description='Password')

    @validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-zA-Z0-9@ ])+$', value):
            raise ValueError('Username format invalid')
        return value

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    detail: str

class UserDetail(BaseModel):
    user_id: UUID
    username: str

class TokenSchema(BaseModel):
    user_id: UUID
    username: str
    isAdmin: Optional[bool]
    access_token: str
    refresh_token: str