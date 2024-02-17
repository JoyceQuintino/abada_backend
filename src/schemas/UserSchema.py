import re
from pydantic import BaseModel, validator

class UserCreateInput(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[A-Z]|[0-9]|@)+$', value):
            raise ValueError('Username format invalid')
        return value

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    detail: str