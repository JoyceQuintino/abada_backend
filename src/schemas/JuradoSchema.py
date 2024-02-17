from pydantic import BaseModel

class JuradoInput(BaseModel):
    nome: str

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    message: str