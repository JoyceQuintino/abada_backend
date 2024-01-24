from pydantic import BaseModel, Field
from src.models.models import Categorias, Jogos, Competidores

class ChaveamentoInput(BaseModel):
    categoria: str = Field(title="Categoria", 
                           description="Categoria que será feita o chaveamento")
    
class ChaveamentoOutput(BaseModel):
    categoria: Categorias = Field(title="Categoria", 
                                  description="Categoria dos participantes de acordo com suas graduações.")
    jogos_fem: [Jogos] = Field(title="Jogos Femininos", 
                               description="Todos os jogos femininos a ocorrer.")
    jogos_masc: [Jogos] = Field(title="Jogos masculinos", 
                                description="Todos os jogos masculinos a ocorrer.")
    competidores_categoria: [Competidores] = Field(title="Competidores", 
                                                   description="Lista de todos os competidores a participar dessa categoria.")
    