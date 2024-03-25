from sqlalchemy.future import select
from src.utils.util import Utils
from src.database.db_connection import async_session
from src.models.models import Competidores, Jogos, Modalidades, Graduacoes, Categorias
from sqlalchemy.orm import class_mapper
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json
import os

FEMININO = 'F'
MASCULINO = 'M'

class ChaveamentoService:
    @staticmethod
    async def get_all_chaveamento():
        file_path = 'src/chaveamento_json/chaveamento.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                json_content = file.read()
            data = json.loads(json_content)
            return JSONResponse(content=data, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="File not found")

    @staticmethod
    async def chaveamento_categoria(categorias: List[str]):
        resultados = {}
        todos_competidores = []
        for categoria in categorias:
            async with async_session() as session:
                result = await session.execute(select(Categorias). \
                    where(Categorias.nome == categoria))
                categoria_obj = result.scalars().all()[0]
                
                result = await session.execute(select(Competidores). \
                    join(Graduacoes).join(Categorias). \
                    where(Categorias.nome == categoria_obj.nome))
                comps = result.scalars().all()

                if comps:
                    result = await session.execute(select(Modalidades))
                    modalidades = result.scalars().all()

                    (comp_fem, comp_masc) = Utils.separate_by_sex(comps)
                    chaves_fem, jogos_fem = await Utils.round_robin(players=comp_fem,
                                                            genero=FEMININO,
                                                            modalidades=modalidades,
                                                            categoria=categoria,
                                                            session=session)
                    chaves_masc, jogos_masc = await Utils.round_robin(players=comp_masc,
                                                            genero=MASCULINO,
                                                            modalidades=modalidades,
                                                            categoria=categoria,
                                                            session=session)
                    
                    session.add_all(jogos_masc + jogos_fem)
                    result = await session.commit()

                    jogos_fem_serialized = [jfem.to_dict() for jfem in jogos_fem]
                    jogos_masc_serialized = [jmasc.to_dict() for jmasc in jogos_masc]

                    for jogo in jogos_fem_serialized:
                        modalidade = jogo["modalidade"]["nome"]
                        chaves_fem[modalidade].append(jogo)

                    for jogo in jogos_masc_serialized:
                        modalidade = jogo["modalidade"]["nome"]
                        chaves_masc[modalidade].append(jogo)

                    chaveamento = {
                        "categoria": categoria,
                        "chaves_fem": chaves_fem,
                        "chaves_masc": chaves_masc
                    }

                    resultados[categoria.replace("-", "_")] = chaveamento

                    todos_competidores.extend(comps)

        resultados["competidores_categoria"] = [competidor.to_dict() for competidor in todos_competidores]
             
        dir_name = 'src/chaveamento_json'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        fileName = os.path.join(dir_name, 'chaveamento.json')

        with open(fileName, 'w') as fileJson:
            json.dump(resultados, fileJson)

        return resultados

    @staticmethod
    async def chaveamento_categoria_teste(categoria: str):
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
            
            (comp_fem, comp_masc) = Utils.separate_by_sex(comps)
            (chaves_fem, jogos_fem) = await Utils.round_robin(players=comp_fem,
                genero=FEMININO,
                modalidades=modalidades,
                categoria=categoria,
                session=session)
            (chaves_masc, jogos_masc) = await Utils.round_robin(players=comp_masc,
                genero=MASCULINO,
                modalidades=modalidades,
                categoria=categoria,
                session=session)
            session.add_all(jogos_masc + jogos_fem)
            result = await session.commit()
            
            return {
                "categoria": categoria,
                "chaves_fem": chaves_fem,
                "chaves_masc": chaves_masc,
                "competidores_categoria": comps
            }
