import random


def divide_players(players):
    divided_players = []
    if len(players) % 2 != 0:
        players.append("")
    for _ in range(len(players) // 4):
        group = random.sample(players, 4)
        for name in group:
            players.remove(name)
        divided_players.append(group)
    return divided_players


def round_robin(players):
    if len(players) % 2 != 0:
        players.append(None)
    num_rounds = len(players) - 1
    matches = []
    for _ in range(num_rounds):
        round_matches = []
        for i in range(len(players) // 2):
            if players[i] is not None and players[-i - 1] is not None:
                match = (players[i], players[-i - 1])
                round_matches.append(match)
        players.insert(1, players.pop())
        matches.append(round_matches)
    return matches
