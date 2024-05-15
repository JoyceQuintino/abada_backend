import random
from typing import List, Optional
import json
from sqlalchemy.future import select
from src.models.models import Jogos, Competidores, Modalidades, Pontuacoes, Categorias, Ranking

FEMININO = 'F'
GENERO = 'genero'
FASE = 'fase'

graduados = [
    "graduadas",
    "azul-azul-verde",
    "verde-verde-roxa",
    "roxa-roxa-marrom",
    "marrom-marrom-vermelha"
]

class Utils:

    @staticmethod
    def separate_by_sex(players: List[Competidores]):
        fem = []
        masc = []
        for player in players:
            if player.sexo == FEMININO:
                fem.append(player)
            else:
                masc.append(player)
        return (fem, masc)

    @staticmethod
    def divide_players(players):
        divided_players = []
        if len(players) < 4:
            divided_players = players
            aux = 4 - len(players)
            if aux:
                for _ in range(aux):
                    divided_players.append(Competidores(nome=None, apelido=None, sexo=None, idade=None, cidade=None, estado=None))
            return divided_players
        if len(players) % 2 != 0:
            players.append(Competidores(nome="", apelido="", sexo="", idade="", cidade="", estado=""))
        for _ in range(len(players) // 4):
            group = random.sample(players, 4)
            for name in group:
                players.remove(name)
            divided_players.append(group)
        return divided_players

    # @staticmethod
    # async def round_robin(players: List, genero: str, modalidades: List, categoria: str, quantidade_competidores: int, fase: str, session):
    #     chaves = {}
    #     jogos = []

    #     categoria_obj = None
    #     result = await session.execute(select(Categorias).filter_by(nome=categoria))
    #     categoria_obj = result.scalar()

    #     if not categoria_obj:
    #         raise ValueError(f"A categoria '{categoria}' não foi encontrada.")

    #     if len(players) < 4:
    #         if len(players) == 0:
    #             players.append(Competidores(nome="", apelido="", cidade="", estado="", id_graduacao=""))
    #         else:
    #             players.append(Competidores(nome=None, apelido=None, cidade=None, estado=None, id_graduacao=players[0].id_graduacao))

    #     is_graduado = categoria in graduados

    #     for index, modalidade in enumerate(modalidades):
    #         print(index, modalidade)
    #         rodada = {}
    #         players_modalidade = players[:quantidade_competidores]

    #         if len(players_modalidade) >= 4:
    #             if index == 0:
    #                 for j in range(0, len(players_modalidade), 2):
    #                     if j + 1 < len(players_modalidade):
    #                         id_competidor_1 = players_modalidade[j].id
    #                         id_competidor_2 = players_modalidade[j+1].id

    #                         jogo = Jogos(id_competidor_1=id_competidor_1,
    #                                      id_competidor_2=id_competidor_2,
    #                                      modalidade=modalidade,
    #                                      categoria=categoria_obj,
    #                                      fase=fase,
    #                                      jogo_order=j+1)
    #                         rodada[f'jogo_{j+1}'] = jogo
    #                         jogos.append(rodada[f'jogo_{j+1}'])
    #             elif index == 1 and is_graduado:
    #                 for j in range(0, len(players_modalidade), 4):
    #                     if j + 3 < len(players_modalidade):
    #                         id_competidor_1 = players_modalidade[j].id
    #                         id_competidor_2 = players_modalidade[j+3].id

    #                         jogo = Jogos(id_competidor_1=id_competidor_1,
    #                                      id_competidor_2=id_competidor_2,
    #                                      modalidade=modalidade,
    #                                      categoria=categoria_obj,
    #                                      fase=fase,
    #                                      jogo_order=j+1)
    #                         rodada[f'jogo_{j+1}'] = jogo
    #                         jogos.append(rodada[f'jogo_{j+1}'])

    #                         id_competidor_1 = players_modalidade[j+1].id
    #                         id_competidor_2 = players_modalidade[j+2].id

    #                         jogo = Jogos(id_competidor_1=id_competidor_1,
    #                                      id_competidor_2=id_competidor_2,
    #                                      modalidade=modalidade,
    #                                      categoria=categoria_obj,
    #                                      fase=fase,
    #                                      jogo_order=j+2)
    #                         rodada[f'jogo_{j+2}'] = jogo
    #                         jogos.append(rodada[f'jogo_{j+2}'])
    #             elif index == 2:
    #                 for j in range(0, len(players_modalidade), 4):
    #                     if j + 3 < len(players_modalidade):
    #                         id_competidor_1 = players_modalidade[j].id
    #                         id_competidor_2 = players_modalidade[j+2].id

    #                         jogo = Jogos(id_competidor_1=id_competidor_1,
    #                                      id_competidor_2=id_competidor_2,
    #                                      modalidade=modalidade,
    #                                      categoria=categoria_obj,
    #                                      fase=fase,
    #                                      jogo_order=j+1)
    #                         rodada[f'jogo_{j+1}'] = jogo
    #                         jogos.append(rodada[f'jogo_{j+1}'])

    #                         id_competidor_1 = players_modalidade[j+1].id
    #                         id_competidor_2 = players_modalidade[j+3].id

    #                         jogo = Jogos(id_competidor_1=id_competidor_1,
    #                                      id_competidor_2=id_competidor_2,
    #                                      modalidade=modalidade,
    #                                      categoria=categoria_obj,
    #                                      fase=fase,
    #                                      jogo_order=j+2)
    #                         rodada[f'jogo_{j+2}'] = jogo
    #                         jogos.append(rodada[f'jogo_{j+2}'])
    #         else:
    #             # Para menos de 4 jogadores, a lógica permanece a mesma das modalidades seguintes
    #             for j in range(0, len(players_modalidade), 4):
    #                 if j + 3 < len(players_modalidade):
    #                     id_competidor_1 = players_modalidade[j].id
    #                     id_competidor_2 = players_modalidade[j+2].id

    #                     jogo = Jogos(id_competidor_1=id_competidor_1,
    #                                  id_competidor_2=id_competidor_2,
    #                                  modalidade=modalidade,
    #                                  categoria=categoria_obj,
    #                                  fase=fase,
    #                                  jogo_order=j+1)
    #                     rodada[f'jogo_{j+1}'] = jogo
    #                     jogos.append(rodada[f'jogo_{j+1}'])

    #                     id_competidor_1 = players_modalidade[j+1].id
    #                     id_competidor_2 = players_modalidade[j+3].id

    #                     jogo = Jogos(id_competidor_1=id_competidor_1,
    #                                  id_competidor_2=id_competidor_2,
    #                                  modalidade=modalidade,
    #                                  categoria=categoria_obj,
    #                                  fase=fase,
    #                                  jogo_order=j+2)
    #                     rodada[f'jogo_{j+2}'] = jogo
    #                     jogos.append(rodada[f'jogo_{j+2}'])

    #         if jogos:
    #             chaves[FASE] = fase
    #             chaves[GENERO] = 'Feminino' if genero == FEMININO else 'Masculino'
    #             chaves[f'{modalidade.nome}'] = []

    #     return (chaves, jogos)

    @staticmethod
    async def round_robin(players: List, genero: str, modalidades: List, categoria: str, quantidade_competidores: int, fase: str, session):
        chaves = {}
        jogos = []

        # Recupera a categoria do banco de dados
        result = await session.execute(select(Categorias).filter_by(nome=categoria))
        categoria_obj = result.scalar()

        if not categoria_obj:
            raise ValueError(f"A categoria '{categoria}' não foi encontrada.")

        # Se o número de jogadores for menor que a quantidade desejada, adiciona jogadores fictícios (byes)
        while len(players) < quantidade_competidores:
            players.append(Competidores(nome="BYE", apelido="BYE", cidade="", estado="", id_graduacao=""))

        is_graduado = categoria in graduados

        for index, modalidade in enumerate(modalidades):
            rodada = {}
            players_modalidade = players[:quantidade_competidores]

            if len(players_modalidade) >= 4:
                if index == 0:
                    # Modalidade 1: Jogos entre pares consecutivos
                    for j in range(0, len(players_modalidade), 2):
                        if j + 1 < len(players_modalidade):
                            id_competidor_1 = players_modalidade[j].id
                            id_competidor_2 = players_modalidade[j + 1].id

                            jogo = Jogos(id_competidor_1=id_competidor_1,
                                         id_competidor_2=id_competidor_2,
                                         modalidade=modalidade,
                                         categoria=categoria_obj,
                                         fase=fase,
                                         jogo_order=j + 1)
                            rodada[f'jogo_{j + 1}'] = jogo
                            jogos.append(rodada[f'jogo_{j + 1}'])

                elif index == 1 and is_graduado:
                    # Modalidade 2: Jogos entre pares específicos (para graduados)
                    for j in range(0, len(players_modalidade), 4):
                        if j + 3 < len(players_modalidade):
                            id_competidor_1 = players_modalidade[j].id
                            id_competidor_2 = players_modalidade[j + 3].id

                            jogo = Jogos(id_competidor_1=id_competidor_1,
                                         id_competidor_2=id_competidor_2,
                                         modalidade=modalidade,
                                         categoria=categoria_obj,
                                         fase=fase,
                                         jogo_order=len(jogos) + 1)
                            rodada[f'jogo_{len(jogos) + 1}'] = jogo
                            jogos.append(rodada[f'jogo_{len(jogos) + 1}'])

                            if j + 2 < len(players_modalidade):
                                id_competidor_1 = players_modalidade[j + 1].id
                                id_competidor_2 = players_modalidade[j + 2].id

                                jogo = Jogos(id_competidor_1=id_competidor_1,
                                             id_competidor_2=id_competidor_2,
                                             modalidade=modalidade,
                                             categoria=categoria_obj,
                                             fase=fase,
                                             jogo_order=len(jogos) + 1)
                                rodada[f'jogo_{len(jogos) + 1}'] = jogo
                                jogos.append(rodada[f'jogo_{len(jogos) + 1}'])

                    # Verificação adicional para número de jogadores não múltiplo de 4
                    if len(players_modalidade) % 4 != 0:
                        # Pegue os dois últimos jogadores
                        jogadores_restantes = players_modalidade[-2:]
                        ultimo_jogo = jogos[-1]

                        # Crie dois novos jogos com os dois jogadores restantes e os jogadores do último jogo
                        novo_jogo_1 = Jogos(id_competidor_1=ultimo_jogo.id_competidor_1,
                                            id_competidor_2=jogadores_restantes[0].id,
                                            modalidade=modalidade,
                                            categoria=categoria_obj,
                                            fase=fase,
                                            jogo_order=len(jogos))  # manter a ordem do último jogo original

                        novo_jogo_2 = Jogos(id_competidor_1=ultimo_jogo.id_competidor_2,
                                            id_competidor_2=jogadores_restantes[1].id,
                                            modalidade=modalidade,
                                            categoria=categoria_obj,
                                            fase=fase,
                                            jogo_order=len(jogos) + 1)

                        # Substitua o último jogo original pelo primeiro novo jogo
                        jogos[-1] = novo_jogo_1
                        # Adicione o segundo novo jogo
                        jogos.append(novo_jogo_2)

                elif index == 2:
                    # Modalidade 3: Jogos entre outros pares específicos
                    for j in range(0, len(players_modalidade), 4):
                        if j + 2 < len(players_modalidade):
                            id_competidor_1 = players_modalidade[j].id
                            id_competidor_2 = players_modalidade[j + 2].id

                            jogo = Jogos(id_competidor_1=id_competidor_1,
                                         id_competidor_2=id_competidor_2,
                                         modalidade=modalidade,
                                         categoria=categoria_obj,
                                         fase=fase,
                                         jogo_order=len(jogos) + 1)
                            rodada[f'jogo_{len(jogos) + 1}'] = jogo
                            jogos.append(rodada[f'jogo_{len(jogos) + 1}'])

                        if j + 3 < len(players_modalidade):
                            id_competidor_1 = players_modalidade[j + 1].id
                            id_competidor_2 = players_modalidade[j + 3].id

                            jogo = Jogos(id_competidor_1=id_competidor_1,
                                         id_competidor_2=id_competidor_2,
                                         modalidade=modalidade,
                                         categoria=categoria_obj,
                                         fase=fase,
                                         jogo_order=len(jogos) + 1)
                            rodada[f'jogo_{len(jogos) + 1}'] = jogo
                            jogos.append(rodada[f'jogo_{len(jogos) + 1}'])

                    # Verificação adicional para número de jogadores não múltiplo de 4
                    if len(players_modalidade) % 4 != 0:
                        # Pegue os dois últimos jogadores
                        jogadores_restantes = players_modalidade[-2:]
                        ultimo_jogo = jogos[-1]

                        # Crie dois novos jogos com os dois jogadores restantes e os jogadores do último jogo
                        novo_jogo_1 = Jogos(id_competidor_1=ultimo_jogo.id_competidor_1,
                                            id_competidor_2=jogadores_restantes[0].id,
                                            modalidade=modalidade,
                                            categoria=categoria_obj,
                                            fase=fase,
                                            jogo_order=len(jogos))  # manter a ordem do último jogo original

                        novo_jogo_2 = Jogos(id_competidor_1=ultimo_jogo.id_competidor_2,
                                            id_competidor_2=jogadores_restantes[1].id,
                                            modalidade=modalidade,
                                            categoria=categoria_obj,
                                            fase=fase,
                                            jogo_order=len(jogos) + 1)

                        # Substitua o último jogo original pelo primeiro novo jogo
                        jogos[-1] = novo_jogo_1
                        # Adicione o segundo novo jogo
                        jogos.append(novo_jogo_2)

            else:
                # Para menos de 4 jogadores, aplica uma lógica diferente
                for j in range(0, len(players_modalidade), 2):
                    if j + 1 < len(players_modalidade):
                        id_competidor_1 = players_modalidade[j].id
                        id_competidor_2 = players_modalidade[j + 1].id

                        jogo = Jogos(id_competidor_1=id_competidor_1,
                                     id_competidor_2=id_competidor_2,
                                     modalidade=modalidade,
                                     categoria=categoria_obj,
                                     fase=fase,
                                     jogo_order=j + 1)
                        rodada[f'jogo_{j + 1}'] = jogo
                        jogos.append(rodada[f'jogo_{j + 1}'])

            if jogos:
                chaves[FASE] = fase
                chaves[GENERO] = 'Feminino' if genero == FEMININO else 'Masculino'
                chaves[f'{modalidade.nome}'] = []

        return (chaves, jogos)