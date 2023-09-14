from pydantic import BaseModel

class JuradoCreateInput(BaseModel):
    nome: str

class StandardOutput(BaseModel):
    message: str