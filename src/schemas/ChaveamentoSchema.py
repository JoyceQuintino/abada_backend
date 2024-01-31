from pydantic import BaseModel, Field, ConfigDict
from src.models.models import Categorias, Jogos, Competidores
from typing import List, Optional
from dataclasses import dataclass


class ChaveamentoInput(BaseModel):
    categoria: str = Field(title="Categoria",
                           description="Categoria que será feita o chaveamento")


class ChaveamentoOutput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    categoria: str = Field(title="Categoria", description="Categoria que ocorreu o chaveamento")
    jogos_fem: List[List[Jogos]] = Field(title="Jogos fem", description="Lista de jogos femininos")
    jogos_masc: List[List[Jogos]] = Field(title="Jogos masc", description="Lista de jogos masculinos")
    competidores_categoria: List[Competidores] = Field(title="Competidores", description="Lista de competidores da categoria")
