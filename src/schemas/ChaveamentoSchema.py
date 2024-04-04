from pydantic import BaseModel, Field, ConfigDict
from src.models.models import Categorias, Jogos, Competidores
from typing import List, Optional
from dataclasses import dataclass
class CategoriaInput(BaseModel):
    nome: str
    modalidade: Optional[str] = None
    quantidade_competidores: Optional[int] = None
    fase: Optional[int] = None
class ChaveamentoInput(BaseModel):
    categorias: List[CategoriaInput]
    token: str

# class ChaveamentoInput(BaseModel):
#     categoria: List[str] = Field(title="Categoria",
#                            description="Categoria que será feita o chaveamento")
#     token: str