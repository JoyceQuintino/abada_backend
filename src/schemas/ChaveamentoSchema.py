from pydantic import BaseModel, Field
from src.models.models import Categorias, Jogos, Competidores
from typing import List, Optional

class ChaveamentoInput(BaseModel):
    categoria: str = Field(title="Categoria",
                           description="Categoria que será feita o chaveamento")
