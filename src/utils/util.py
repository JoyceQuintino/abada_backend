import random
from typing import List, Optional
from src.models.models import Jogos, Competidores, Modalidades, Pontuacoes, Jurados, Categorias

class Utils:

    @staticmethod
    def separate_by_sex(players: List[Competidores]):
        fem = []
        masc = []
        for player in players:
            if player.sexo == 'F':
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
                    divided_players.append(Competidores(nome="", apelido="", sexo="", idade="", cidade="", estado=""))
            return divided_players
        if len(players) % 2 != 0:
            players.append(Competidores(nome="", apelido="", sexo="", idade="", cidade="", estado=""))
        for _ in range(len(players) // 4):
            group = random.sample(players, 4)
            for name in group:
                players.remove(name)
            divided_players.append(group)
        return divided_players


    @staticmethod
    def round_robin(players: List, modalidades: List, categoria: str):
        # print(players)
        chaves = {}
        jogos = []
        if len(players) < 4:
            players.append(Competidores(nome="Nulo", apelido="Nulo", cidade="Nulo", estado="Nulo", id_graduacao=players[0].id_graduacao))
        for i in range(len(players) - 1):
            rodada = {}
            if (modalidades[i].nome == "siriuna") and (categoria == "laranja-laranja-azul"):
                continue
            for j in range(len(players)//2):
                jogo = Jogos(id_competidor_1=players[j].id,
                    id_competidor_2=players[-j-1].id,
                    modalidade=modalidades[i])
                rodada[f'Jogo {j+1}'] = jogo
                jogos.append(rodada[f'Jogo {j+1}'])
            chaves[f'{modalidades[i].nome}'] = rodada
            players.insert(1, players.pop())
        return (chaves, jogos)
        # if len(players) % 2 != 0:
        #     players.append(None)
        # num_rounds = len(players) - 1
        # matches = []
        # for _ in range(num_rounds):
        #     round_matches = []
        #     for i in range(len(players) // 2):
        #         # print(f'{players[i]} - {players[-i-1]}')
        #         if players[i] is not None and players[-i - 1] is not None:
        #             match = Jogos(id_competidor_1=players[i].id, id_competidor_2=players[(-i - 1)].id, id_modalidade="0acab9fd-e689-447f-8e05-539cd6b1acce", id_categoria="6da9cb61-8a1f-48f9-9c42-545a0ff32a94")
        #             # match = [players[i], players[-i - 1]]
        #             round_matches.append(match)
        #     players.insert(1, players.pop())
        #     matches.append(round_matches)
        # return matches
        # print(players)
        # if len(players) % 2 != 0:
        #     players.append(None)
        # num_rounds = len(players) - 1
        # matches = []
        # for _ in range(num_rounds):
        #     round_matches = []
        #     for i in range(len(players) // 2):
        #         if players[i] is not None and players[-i - 1] is not None:
        #             match = [players[i], players[(-i - 1)]]
        #             round_matches.append(match)
        #     players.insert(1, players.pop())
        #     matches.append(round_matches)
        #     # print(round_matches.)
        # return matches
