import random
from src.models.models import Jogos, Competidores, Modalidades, Pontuacoes, Jurados


def separate_by_sex(players: list):
    fem = []
    masc = []
    for player in players:
        if player.sexo == 'F':
            fem.append(player)
        else:
            masc.append(player)
    return fem, masc

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


def round_robin(players: list[Competidores]):
    if len(players) % 2 != 0:
        players.append(None)
    num_rounds = len(players) - 1
    matches = []
    for _ in range(num_rounds):
        round_matches = []
        for i in range(len(players) // 2):
            if players[i] is not None and players[-i - 1] is not None:
                # match = Jogo(id_competidor_1=players[i].id, id_competidor_2=players[(-i - 1)].id, nota=0)
                match = (players[i], players[-i - 1])
                round_matches.append(match)
        players.insert(1, players.pop())
        matches.append(round_matches)
    return matches
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
