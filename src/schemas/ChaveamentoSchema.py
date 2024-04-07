from pydantic import BaseModel
from typing import List, Optional, Dict

class ModalidadeInput(BaseModel):
    genero: str
    quantidade_competidores: Optional[int] = None
    fase: Optional[int] = None

class CategoriaInput(BaseModel):
    nome: str
    modalidades: Dict[str, ModalidadeInput]

class ChaveamentoInput(BaseModel):
    categorias: List[CategoriaInput]
    token: str
