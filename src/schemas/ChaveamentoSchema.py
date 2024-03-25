from pydantic import BaseModel, Field, ConfigDict
from src.models.models import Categorias, Jogos, Competidores
from typing import List
from dataclasses import dataclass

class ChaveamentoInput(BaseModel):
    categoria: List[str] = Field(title="Categoria",
                           description="Categoria que será feita o chaveamento")
    token: str
