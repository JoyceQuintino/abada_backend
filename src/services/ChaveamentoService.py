from sqlalchemy import desc
from typing import List
from sqlalchemy.future import select
from src.utils.util import Utils
from src.database.db_connection import async_session
from src.models.models import Competidores, Jogos, Modalidades, Graduacoes, Categorias
from random import sample

FEMININO = 'F'
MASCULINO = 'M'

class ChaveamentoService:

    @staticmethod
    async def chaveamento_categoria(categoria: str):
        async with async_session() as session:
            result = await session.execute(select(Categorias). \
                where(Categorias.nome == categoria))
            categoria_obj = result.scalars().all()[0]
            result = await session.execute(select(Modalidades))
            modalidades = result.scalars().all()
            result = await session.execute(select(Competidores). \
                join(Graduacoes).join(Categorias). \
                where(Categorias.nome == categoria_obj.nome))
            comps = result.scalars().all()
            #TODO: Chamar funções para separação de sexo e posteriormente para divisao dos jogos
            (comp_fem, comp_masc) = Utils.separate_by_sex(comps)
            (chaves_fem, jogos_fem) = Utils.round_robin(players=comp_fem,
                                                        genero=FEMININO,
                                                        modalidades=modalidades,
                                                        categoria=categoria)
            (chaves_masc, jogos_masc) = Utils.round_robin(players=comp_masc,
                                                          genero=MASCULINO,
                                                          modalidades=modalidades,
                                                          categoria=categoria)
            session.add_all(jogos_masc + jogos_fem)
            result = await session.commit()
            return {
                "categoria": categoria,
                "chaves_fem": chaves_fem,
                "chaves_masc": chaves_masc,
                "competidores_categoria": comps
            }
