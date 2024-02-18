import re
from pydantic import BaseModel, validator, Field

class UserCreateInput(BaseModel):
    username: str = Field(..., min_length=5, max_length=50, description='Username')
    password: str = Field(..., min_length=5, max_length=20, description='Password')

    @validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[A-Z]|[0-9]|@)+$', value):
            raise ValueError('Username format invalid')
        return value

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    detail: str