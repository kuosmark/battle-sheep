import copy
from typing import List, Tuple
from game import Game


def get_possible_moves(game: Game) -> List[Game]:
    possible_moves: List[Game] = []
    if game.is_in_initial_placement():
        for pasture in game.get_potential_initial_pastures():
            game.make_initial_turn(pasture)
            possible_moves.append(copy.deepcopy(game))
            game.undo_initial_turn(pasture)
    else:
        for pasture in game.get_potential_sheep_to_move():
            for target_pasture in pasture.get_potential_targets(game.pastures):
                for sheep in range(1, pasture.get_amount_of_sheep()):
                    game.make_normal_turn(pasture, target_pasture, sheep)
                    possible_moves.append(copy.deepcopy(game))
                    game.undo_normal_turn(pasture, target_pasture, sheep)

    # Järjestetään mahdolliset siirrot heuristisen arvon mukaiseen paremmuusjärjestykseen
    return sorted(
        possible_moves, key=lambda move: move.evaluate_game_state(), reverse=game.is_players_turn())


def minimax(game: Game, depth: int, alpha: float, beta: float) -> Tuple[float, Game | None]:
    # Palautetaan pelitilanteen arvo, mikäli päästiin annettuun syvyyteen
    # tai peli on ohi vuorossa olevalta pelaajalta
    if depth == 0 or game.is_over_for_player_in_turn():
        return game.evaluate_game_state(), None

    possible_moves = get_possible_moves(game)
    best_move: Game | None = None

    if game.is_players_turn():
        best_value = float('-Inf')
        for move in possible_moves:
            value, _ = minimax(move, depth - 1, alpha, beta)
            if value > best_value:
                best_value = value
                best_move = move

            if best_value > beta:
                break
            alpha = max(alpha, best_value)
    else:
        best_value = float('Inf')
        for move in possible_moves:
            value, _ = minimax(move, depth - 1, alpha, beta)
            if value < best_value:
                best_value = value
                best_move = move

            if best_value < alpha:
                break
            beta = min(beta, best_value)

    return best_value, best_move
