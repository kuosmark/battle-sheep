import copy
from game import Game
from move import Move

INITIAL_SHEEP = 16


def minimax(game: Game, depth: int):
    # Palautetaan pelitilanteen arvo, mikäli peli on ohi tai päästiin annettuun syvyyteen
    if depth == 0 or game.is_over():
        return game.evaluate_game_state(), None

    # Pelaaja tahtoo maksimoida arvon, tekoäly tahtoo minimoida sen
    value = float('-Inf') if game.is_humans_turn else float('Inf')
    best_move: Move | None = None

    game_copy = copy.deepcopy(game)
    if game_copy.is_in_initial_placement():
        for pasture in game_copy.get_potential_initial_pastures():
            game_copy.make_initial_turn(pasture)
            # Mennään syvemmälle
            value_of_move = minimax(game_copy, depth - 1)[0]
            value = max(value, value_of_move) if game.is_humans_turn else min(
                value, value_of_move)
            if value_of_move == value:
                # Mikäli vuoro on paras löydetyistä, otetaan se talteen
                best_move = Move(pasture, None, INITIAL_SHEEP)
            game_copy.undo_initial_move(pasture)

    else:
        for pasture in game_copy.get_potential_sheep_to_move():
            for target_pasture in pasture.get_potential_targets(game_copy.pastures):
                for amount_of_sheep in range(1, pasture.get_amount_of_sheep()):
                    game_copy.make_normal_turn(
                        pasture, target_pasture, amount_of_sheep)
                    # Mennään syvemmälle
                    value_of_move = minimax(game_copy, depth - 1)[0]
                    value = max(value, value_of_move) if game.is_humans_turn else min(
                        value, value_of_move)
                    if value_of_move == value:
                        # Mikäli vuoro on paras löydetyistä, otetaan se talteen
                        best_move = Move(
                            pasture, target_pasture, amount_of_sheep)
                    game_copy.undo_move(
                        pasture, target_pasture, amount_of_sheep)

    return value, best_move
