from pydantic import BaseModel
from uuid import UUID

class PontuacaoInput(BaseModel):
    pontuacao_competidor_1: float
    pontuacao_competidor_2: float
    pontuacao_jogo: float
    id_jogo: UUID
    jogo_valido: int
    id_user: UUID

class RankingInput(BaseModel):
    apelido: str
    numero: int
    sexo: str
    categoria: str
    fase: int
    id_competidor: UUID
    total_jogo: float
    total_competidor: float
    nota_total: float

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    detail: str