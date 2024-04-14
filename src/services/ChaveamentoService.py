from sqlalchemy.future import select
from src.utils.util import Utils
from src.database.db_connection import async_session
from src.models.models import Competidores, Jogos, Modalidades, Graduacoes, Categorias, Ranking
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
    async def ordenar_jogadores_por_pontuacao(players: List, fase, session):
        players_empty = []

        if fase != 1:
            players_all = await session.execute(select(Ranking.fase).distinct())
            fases_existentes = [row[0] for row in players_all]
            fase_anterior = fase - 1
            if fase_anterior not in fases_existentes:
                print(f'A fase anterior à fase {fase} não existe no ranking.')
                return players_empty
            else:
                players_all = await session.execute(select(Ranking).filter(Ranking.fase == fase_anterior))
                player_scores = {player[0].id_competidor: player[0].nota_total for player in players_all}
                players.sort(key=lambda player: player_scores.get(player.id, 0), reverse=True)
                print("Jogadores ordenados após a ordenação:")
                for player in players:
                    print(player.id)
        return players

    @staticmethod
    async def chaveamento_categoria(categorias: List[CategoriaInput]):
        resultados = {}
        todos_competidores = []

        for categoria_input in categorias:
            async with async_session() as session:
                nome_categoria = categoria_input.nome
                modalidade_categoria = categoria_input.modalidades

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
                    
                    if modalidade_categoria['F'].genero == FEMININO and modalidade_categoria['F'].quantidade_competidores is not None:
                        comp_fem = await ChaveamentoService.ordenar_jogadores_por_pontuacao(comp_fem, modalidade_categoria['F'].fase, session)
                        chaves_fem, jogos_fem = await Utils.round_robin(players=comp_fem,
                                                                        genero=FEMININO,
                                                                        modalidades=modalidades,
                                                                        categoria=nome_categoria,
                                                                        quantidade_competidores=modalidade_categoria['F'].quantidade_competidores,
                                                                        fase=modalidade_categoria['F'].fase,
                                                                        session=session)
                    if modalidade_categoria['M'].genero == MASCULINO and modalidade_categoria['M'].quantidade_competidores is not None:
                        comp_masc = await ChaveamentoService.ordenar_jogadores_por_pontuacao(comp_masc, modalidade_categoria['M'].fase, session)
                        chaves_masc, jogos_masc = await Utils.round_robin(players=comp_masc,
                                                                          genero=MASCULINO,
                                                                          modalidades=modalidades,
                                                                          categoria=nome_categoria,
                                                                          quantidade_competidores=modalidade_categoria['M'].quantidade_competidores,
                                                                          fase=modalidade_categoria['M'].fase,
                                                                          session=session)
                    
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
