from sqlalchemy.future import select
from src.utils.util import Utils
from src.database.db_connection import async_session
from src.models.models import Competidores, Jogos, Modalidades, Graduacoes, Categorias
from src.schemas.ChaveamentoSchema import ChaveamentoInput, CategoriaInput
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json
import os

FEMININO = 'F'
MASCULINO = 'M'
AMBOS = 'All'
GENERO = 'genero'
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
    async def chaveamento_categoria(categorias: List[CategoriaInput]):
        resultados = {}
        todos_competidores = []

        for categoria_input in categorias:
            async with async_session() as session:
                nome_categoria = categoria_input.nome
                modalidade_categoria = categoria_input.modalidade
                quantidade_competidores = categoria_input.quantidade_competidores
                fase_categoria = categoria_input.fase

                result = await session.execute(select(Categorias).where(Categorias.nome == nome_categoria))
                categoria_obj = result.scalars().all()[0]

                result = await session.execute(select(Competidores).join(Graduacoes).join(Categorias).where(Categorias.nome == categoria_obj.nome))
                comps = result.scalars().all()

                if comps:
                    result = await session.execute(select(Modalidades))
                    modalidades = result.scalars().all()

                    (comp_fem, comp_masc) = Utils.separate_by_sex(comps)
                    chaves_fem, chaves_masc = [],[]
                    jogos_fem, jogos_masc = [], []

                    if modalidade_categoria == AMBOS:
                        chaves_fem, jogos_fem = await Utils.round_robin(players=comp_fem,
                                                                        genero=modalidade_categoria,  # Aqui ajustamos o gênero
                                                                        modalidades=modalidades,
                                                                        categoria=nome_categoria,
                                                                        session=session)
                        if(jogos_fem):
                            chaves_fem[GENERO] = 'Feminino'
                        
                        chaves_masc, jogos_masc = await Utils.round_robin(players=comp_masc,
                                                                          genero=modalidade_categoria,  # Aqui ajustamos o gênero
                                                                          modalidades=modalidades,
                                                                          categoria=nome_categoria,
                                                                          session=session)
                        if jogos_masc:
                            chaves_masc[GENERO] = 'Masculino'

                    elif modalidade_categoria == FEMININO:
                        chaves_fem, jogos_fem = await Utils.round_robin(players=comp_fem,
                                                                        genero=modalidade_categoria,  # Aqui ajustamos o gênero
                                                                        modalidades=modalidades,
                                                                        categoria=nome_categoria,
                                                                        session=session)
                        if(jogos_fem):
                            chaves_fem[GENERO] = 'Feminino'
                
                    elif modalidade_categoria == MASCULINO:
                        chaves_masc, jogos_masc = await Utils.round_robin(players=comp_masc,
                                                                          genero=modalidade_categoria,  # Aqui ajustamos o gênero
                                                                          modalidades=modalidades,
                                                                          categoria=nome_categoria,
                                                                          session=session)
                        if jogos_masc:
                            chaves_masc[GENERO] = 'Masculino'
                    
                    session.add_all(jogos_masc + jogos_fem)
                    result = await session.commit()

                    jogos_fem_serialized = [jfem.to_dict() for jfem in jogos_fem]
                    jogos_masc_serialized = [jmasc.to_dict() for jmasc in jogos_masc]

                    for jogo in jogos_fem_serialized:
                        modalidade = jogo["modalidade"]["nome"]
                        if jogos_fem_serialized:
                            chaves_fem[modalidade].append(jogo)

                    for jogo in jogos_masc_serialized:
                        modalidade = jogo["modalidade"]["nome"]
                        if jogos_masc_serialized:
                            chaves_masc[modalidade].append(jogo)

                    chaveamento = {
                        "categoria": nome_categoria,
                        "chaves_fem": chaves_fem,
                        "chaves_masc": chaves_masc
                    }

                    resultados[nome_categoria.replace("-", "_")] = chaveamento

                    todos_competidores.extend(comps)

        resultados["competidores_categoria"] = [competidor.to_dict() for competidor in todos_competidores]

        dir_name = 'src/chaveamento_json'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        fileName = os.path.join(dir_name, 'chaveamento.json')

        with open(fileName, 'w') as fileJson:
            json.dump(resultados, fileJson)

        return resultados
