import copy
from game import Game

INITIAL_SHEEP = 16


def calculate_ai_move(game: Game):
    depth = 2  # Syvyys 3 on toistaiseksi vielä liian raskas
    # Tekoäly tahtoo minimoida arvon
    value = float('Inf')  # Pelitilanteen heuristinen arvo
    best_pasture = None
    best_target = None
    best_amount = None
    game_copy = copy.deepcopy(game)
    if game_copy.is_in_initial_placement():
        for pasture in game_copy.get_potential_initial_pastures():
            # Jotta saadaan edes jokin siirto pelin päätöstilanteessa
            if best_pasture is None:
                best_pasture = pasture
            game_copy.make_initial_turn(pasture)
            # Mennään syvemmälle
            minimax_value = minimax(game_copy, depth - 1)
            game_copy.undo_initial_move(pasture)
            if (minimax_value < value):
                best_pasture = pasture
                best_target = None
                best_amount = INITIAL_SHEEP
                value = minimax_value

    else:
        for pasture in game_copy.get_potential_sheep_to_move():
            for target_pasture in pasture.get_potential_targets(game_copy.pastures):
                for amount_of_sheep in range(1, pasture.get_amount_of_sheep()):
                    # Jotta saadaan edes jokin siirto pelin päätöstilanteessa
                    if best_pasture is None:
                        best_pasture = pasture
                        best_target = target_pasture
                        best_amount = amount_of_sheep

                    game_copy.make_normal_turn(
                        pasture, target_pasture, amount_of_sheep)
                    # Mennään syvemmälle
                    minimax_value = minimax(game_copy, depth - 1)
                    game_copy.undo_move(
                        pasture, target_pasture, amount_of_sheep)
                    if (minimax_value < value):
                        best_pasture = pasture
                        best_target = target_pasture
                        best_amount = amount_of_sheep
                        value = minimax_value

    print('Valittu arvo on ' + str(value))
    return (best_pasture, best_target, best_amount)


def minimax(game, depth: int) -> float:
    if depth == 0:
        return game.evaluate_game_state()

    game_copy = copy.deepcopy(game)
    if game.is_humans_turn:  # Pelaaja tahtoo maksimoida arvon
        value = float('-Inf')  # Pelitilanteen heuristinen arvo

        for pasture in game_copy.get_potential_sheep_to_move():
            for target_pasture in pasture.get_potential_targets(game_copy.pastures):
                for amount_of_sheep in range(1, pasture.get_amount_of_sheep()):
                    game_copy.make_normal_turn(
                        pasture, target_pasture, amount_of_sheep)
                    # Mennään syvemmälle
                    value = max(value, minimax(game_copy, depth - 1))
                    game_copy.undo_move(
                        pasture, target_pasture, amount_of_sheep)

        return value

    # Tekoäly tahtoo minimoida arvon
    value = float('Inf')  # Pelitilanteen heuristinen arvo

    for pasture in game_copy.get_potential_sheep_to_move():
        for target_pasture in pasture.get_potential_targets(game_copy.pastures):
            for amount_of_sheep in range(1, pasture.get_amount_of_sheep()):
                game_copy.make_normal_turn(
                    pasture, target_pasture, amount_of_sheep)
                # Mennään syvemmälle
                value = min(value, minimax(game_copy, depth - 1))
                game_copy.undo_move(pasture, target_pasture, amount_of_sheep)

    return value
