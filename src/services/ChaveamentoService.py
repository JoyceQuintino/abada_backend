from sqlalchemy import desc
from typing import List
from sqlalchemy.future import select
from src.utils.util import round_robin, divide_players, separate_by_sex
from pydantic import TypeAdapter
from src.database.db_connection import async_session
from src.models.models import Competidores, Jogos, Modalidades, Graduacoes, Categorias
from random import sample


class ChaveamentoService:

    @staticmethod
    async def chaveamento_categoria(categoria: str):
        async with async_session() as session:
            result = await session.execute(select(Competidores).join(Graduacoes).join(Categorias).where(Categorias.nome == categoria))
            competidores = result.scalars().all()
            #TODO: Chamar funções para separação de sexo e posteriormente para divisao dos jogos
            return {
                "categoria": {},
                "jogos_fem": [[]],
                "jogos_masc": [[]],
                "competidores_categoria": []
            }


    async def qualifiers_matches(self):
        async with async_session() as session:
            competidores = {}
            result = await session.execute(select(Modalidades))
            modalidades = result.scalars().all()
            result = await session.execute(select(Categorias))
            categorias = result.scalars().all()
            divided_sex = separate_by_sex(competidores)
            divisao_feminina = divide_players(divided_sex[0])
            # print(divisao_feminina)
            divisao_masculina = divide_players(divided_sex[1])
            matches_masc = []
            matches_fem = []
            jogos_masc = []
            jogos_fem = []
            print(categorias)
            for categoria in categorias:
                result = await session.execute(select(Graduacoes).where(Graduacoes.id_categoria == categoria.id))
                # competidores[categoria.nome] = result.scalars().all()
            return result.scalars().all()
            for modalidade in modalidades:
                for group in divisao_masculina:
                    if not isinstance(group, list):
                        match_groups = round_robin(divisao_masculina)
                        matches_masc.append(match_groups[0])
                        matches_masc.append(match_groups[1])
                        jogo = Jogos(nota=0,
                              jogo_valido=True,
                              id_competidor_1=match_groups[0].id,
                              id_competidor_2=match_groups[1].id,
                              id_modalidade=modalidade.id)
                        jogos_masc.append(jogo)
                        break
                    match_groups = round_robin(group)
                    for item in match_groups:
                        for element in item:
                            print(element)
                            jogo = Jogos(nota=0,
                                  jogo_valido=True,
                                  id_competidor_1=element[0].id,
                                  id_competidor_2=element[1].id,
                                  id_modalidade=modalidade.id)
                            jogos_masc.append(jogo)
                            matches_masc.append(element)
            for group in divisao_feminina:
                if not isinstance(group, list):
                    match_groups = round_robin(divisao_feminina)
                    for item in match_groups:
                        for element in item:
                            matches_fem.append(element)
                            jogo = Jogos(nota=0,
                                         jogo_valido=True,
                                         id_competidor_1=element[0].id,
                                         id_competidor_2=element[1].id,
                                         id_modalidade=modalidade.id)
                            session.add(jogo)
                            jogos_fem.append(jogo)
                    break
                match_groups = round_robin(group)
                for item in match_groups:
                    for element in item:
                        matches_fem.append(element)
                        jogo = Jogos(nota=0,
                              jogo_valido=True,
                              id_competidor_1=element[0].id,
                              id_competidor_2=element[1].id,
                              id_modalidade=modalidade.id)
                        jogos_fem.append(jogo)
            # session.add_all(jogos_masc + jogos_fem)
            # await session.commit()
            return {
                "jogos_masc": jogos_masc,
                "jogos_fem": jogos_fem,
                "partidas_masc": matches_masc,
                "partidas_fem": matches_fem
            }




    async def qualifiers(self):
        async with async_session() as session:
            result = await session.execute(select(Jogos))
            jogos_competidores = []
            for jogo in result.scalars().all():
                competidor_1 = await session.execute(select(Competidores).filter(jogo.id_competidor_1 == Competidores.id))
                competidor_2 = await session.execute(select(Competidores).filter(jogo.id_competidor_2 == Competidores.id))
                jogos_competidores.append([jogo,
                                       competidor_1.scalars().all(),
                                       competidor_2.scalars().all()])
            return jogos_competidores


    async def semifinals(self):
        async with async_session() as session:
            result = await session.execute(select(Competidores).order_by(desc(Competidores.nome)).limit(8))
            return result.scalars().all()

    async def finals(self):
        async with async_session() as session:
            result = await session.execute(select(Competidores).order_by(desc(Competidores.nome)).limit(4))
            return result.scalars().all()

    async def final(self):
        pass
