from sqlalchemy import desc
from sqlalchemy.future import select
from src.utils.util import round_robin, divide_players, separate_by_sex

from src.database.db_connection import async_session 
from src.models.models import Competidores, Jogos, Modalidades


class ChaveamentoService:
    async def qualifiers_matches(self):
        async with async_session() as session:
            result = await session.execute(select(Competidores))
            competidores = result.scalars().all()
            result = await session.execute(select(Modalidades))
            modalidades = result.scalars().all()
            # print(f'{modalidades}\n{competidores}')
            divided_sex = separate_by_sex(competidores)
            divisao_feminina = divide_players(divided_sex[0])
            divisao_masculina = divide_players(divided_sex[1])
            # print(f'divisao feminina: {divisao_feminina}\n')
            # print(f'divisao masculina: {divisao_masculina}')
            matches_masc = []
            matches_fem = []
            # Jogos(nota=0,
            #       jogo_valido=0,
            #       id_competidor_1=players[i].id,
            #       id_competidor_2=players[-i - 1].id,
            #       id_modalidade=modalidades[0].id,
            #       id_pontuacao=pontuacao.id)
            for group in divisao_masculina:
                if not isinstance(group, list):
                    match_groups = round_robin(divisao_masculina)
                    matches_masc.append(match_groups[0])
                    matches_masc.append(match_groups[1])
                    break
                match_groups = round_robin(group)
                for item in match_groups:
                    for element in item:
                        print(element)
                        matches_masc.append(element)
            return matches_masc
            # for group in divisao_feminina:
            #     if not isinstance(group, list):
            #         match_groups = round_robin(divisao_feminina, modalidades)
            #         matches_fem.append(match_groups[0])
            #         matches_fem.append(match_groups[1])
            #         break
            #     match_groups = round_robin(group, modalidades)
            #     matches_fem.append(match_groups[0])
            #     matches_fem.append(match_groups[1])
            # for match in matches_masc and matches_fem:
            #     result = await session.execute(select(Jogos))
            #     jogos = result.scalars().all()
            #     print(jogos)
            #     if match[0] not in jogos and match[1] not in jogos:
            #         session.add_all([match[0], match[1]])
            #         await session.commit()
            # return matches_masc, matches_fem



    async def qualifiers(self):
        async with async_session() as session:
            result = await session.execute(select(Jogos))
            jogos_competidores = []
            for jogo in result.scalars().all():
                competidor_1 = await session.execute(select(Competidores).filter(jogo.id_competidor_1 == Competidor.id))
                competidor_2 = await session.execute(select(Competidores).filter(jogo.id_competidor_2 == Competidor.id))
                jogos_competidores.append([jogo,
                                       competidor_1.scalars().all(),
                                       competidor_2.scalars().all()])
            return jogos_competidores


    async def semifinals(self):
        async with async_session() as session:
            result = await session.execute(select(Competidores).order_by(desc(Competidores.nome)).limit(8))
            return result.scalars().all()

    async def final(self):
        pass
