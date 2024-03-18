import random
from typing import List, Optional
from src.models.models import Jogos, Competidores, Modalidades, Pontuacoes, Categorias

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
    def round_robin(players: List, genero: str, modalidades: List, categoria: str):
        chaves = {}
        jogos = []
        
        if len(players) < 4:
            if len(players) == 0:
                players.append(Competidores(nome="", apelido="", cidade="", estado="", id_graduacao=""))
            else:
                players.append(Competidores(nome="Nulo", apelido="Nulo", cidade="Nulo", estado="Nulo", id_graduacao=players[0].id_graduacao))
        for i in range(len(players) - 1):
            rodada = {}
            if (modalidades[i].nome == "siriuna") and (categoria == "laranja-laranja-azul"):
                continue
            for j in range(len(players)//2):
                jogo = Jogos(id_competidor_1=players[j].id,
                    id_competidor_2=players[-j-1].id,
                    modalidade=modalidades[i])
                rodada[f'jogo_{j+1}'] = jogo
                jogos.append(rodada[f'jogo_{j+1}'])
            
            if genero == 'F':
                chaves['genero'] = 'Feminino'
            else:
                chaves['genero'] = 'Masculino'

            chaves[f'{modalidades[i].nome}'] = rodada
            players.insert(1, players.pop())
        return (chaves, jogos)
