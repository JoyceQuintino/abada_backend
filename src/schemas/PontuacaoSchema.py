from pydantic import BaseModel
from uuid import UUID

class PontuacaoInput(BaseModel):
    pontuacao_competidor_1: float
    pontuacao_competidor_2: float
    pontuacao_jogo: float
    id_jogo: UUID
    id_user: UUID

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    detail: str