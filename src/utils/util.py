import random
from typing import List, Optional
import json
from sqlalchemy.future import select
from src.models.models import Jogos, Competidores, Modalidades, Pontuacoes, Categorias

FEMININO = 'F'
GENERO = 'genero'
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

    @staticmethod
    async def round_robin(players: List, genero: str, modalidades: List, categoria: str, session):
        chaves = {}
        jogos = []
        jogos_com_nulo = []
        jogos_ok = []

        categoria_obj = None
        result = await session.execute(select(Categorias).filter_by(nome=categoria))
        categoria_obj = result.scalar()

        if not categoria_obj:
            raise ValueError(f"A categoria '{categoria}' não foi encontrada.")

        if len(players) < 4:
            if len(players) == 0:
                players.append(Competidores(nome="", apelido="", cidade="", estado="", id_graduacao=""))
            else:
                players.append(Competidores(nome=None, apelido=None, cidade=None, estado=None, id_graduacao=players[0].id_graduacao))
        
        for modalidade in modalidades:
            if categoria == "laranja-laranja-azul" and modalidade.nome == "siriuna":
                continue
            rodada = {}
            for j in range(len(players) // 2):
                id_competidor_1 = players[j].id
                id_competidor_2 = players[-j-1].id

                jogo = Jogos(id_competidor_1=id_competidor_1,
                             id_competidor_2=id_competidor_2,
                             modalidade=modalidade,
                             categoria=categoria_obj)
                rodada[f'jogo_{j+1}'] = jogo
                jogos.append(rodada[f'jogo_{j+1}'])
        
            if jogos:
                if genero == FEMININO:
                    chaves[GENERO] = 'Feminino'
                else:
                    chaves[GENERO] = 'Masculino'
            
                chaves[f'{modalidade.nome}'] = []

            players.insert(1, players.pop())

        for jogo in jogos:
            if jogo.id_competidor_1 is None or jogo.id_competidor_2 is None:
                jogos_com_nulo.append(jogo)
                print(jogo)

        jogos_ok = [jogo for jogo in jogos if jogo not in jogos_com_nulo]

        jogos_ok.extend(jogos_com_nulo)

        if not jogos_ok:
            return (chaves,jogos_ok)

        if len(jogos_ok) == 3:
            primeiro_jogo = jogos_ok[0]
            for jogo in jogos_ok:
                if jogo.id_competidor_1 is None:
                    if jogo.id_competidor_2 != primeiro_jogo.id_competidor_1:
                        jogo.id_competidor_1 = primeiro_jogo.id_competidor_1
                    else:
                        jogo.id_competidor_1 = primeiro_jogo.id_competidor_2
                if jogo.id_competidor_2 is None:
                    if jogo.id_competidor_1 != primeiro_jogo.id_competidor_2:
                        jogo.id_competidor_2 = primeiro_jogo.id_competidor_2
                    else:
                        jogo.id_competidor_2 = primeiro_jogo.id_competidor_1

        return (chaves, jogos_ok)
