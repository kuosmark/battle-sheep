import copy
from game import Game

INITIAL_SHEEP = 16


def calculate_ai_move(game: Game):
    depth = 3
    # Tekoäly tahtoo minimoida arvon
    value = float('Inf')  # Pelitilanteen heuristinen arvo
    best_pasture = None
    best_target = None
    best_amount = None
    if game.is_in_initial_placement():
        for pasture in game.get_potential_initial_pastures():
            current_game = copy.deepcopy(game)
            current_game.make_initial_turn(pasture)
            # Mennään syvemmälle
            minimax_value = minimax(current_game, depth - 1)
            if (minimax_value < value):
                best_pasture = pasture
                best_target = None
                best_amount = INITIAL_SHEEP
                value = minimax_value

    else:
        for pasture in game.get_potential_sheep_to_move():
            for target_pasture in pasture.get_potential_targets(game.pastures):
                for amount_of_sheep in range(1, pasture.get_amount_of_sheep()):
                    current_game = copy.deepcopy(game)
                    current_game.make_normal_turn(
                        pasture, target_pasture, amount_of_sheep)
                    # Mennään syvemmälle
                    minimax_value = minimax(current_game, depth - 1)
                    if (minimax_value < value):
                        best_pasture = pasture
                        best_target = target_pasture
                        best_amount = amount_of_sheep
                        value = minimax_value

    print(best_pasture)
    print(best_target)
    print(best_amount)
    print(best_pasture in game.pastures)
    return (best_pasture, best_target, best_amount)


# Minimax-algoritmi
# Muuttuja game sisältää laudan pelitilanteen, lampaiden sijainnit ja määrät.
# Muuttuja depth on syvyys, johon saakka pelitilanteet käydään läpi.
# is_max_player == is_human_player


def minimax(game, depth: int) -> float:
    print(str(game))
    if depth == 0:
        return game.evaluate_game_state()

    if game.is_humans_turn:  # Pelaaja tahtoo maksimoida arvon
        value = float('-Inf')  # Pelitilanteen heuristinen arvo

        for pasture in game.get_potential_sheep_to_move():
            for target_pasture in pasture.get_potential_targets(game.pastures):
                for amount_of_sheep in range(1, pasture.get_amount_of_sheep()):
                    current_game = copy.deepcopy(game)
                    current_game.make_normal_turn(
                        pasture, target_pasture, amount_of_sheep)
                    # Mennään syvemmälle
                    value = max(value, minimax(current_game, depth - 1))

        return value

    # Tekoäly tahtoo minimoida arvon
    value = float('Inf')  # Pelitilanteen heuristinen arvo

    for pasture in game.get_potential_sheep_to_move():
        for target_pasture in pasture.get_potential_targets(game.pastures):
            for amount_of_sheep in range(1, pasture.get_amount_of_sheep()):
                current_game = copy.deepcopy(game)
                current_game.make_normal_turn(
                    pasture, target_pasture, amount_of_sheep)
                # Mennään syvemmälle
                value = min(value, minimax(current_game, depth - 1))

    return value
