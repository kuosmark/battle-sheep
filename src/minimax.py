import copy
import time
from typing import List, Tuple
from constants import ALPHA, BETA, DEPTH
from game import Game


def get_computers_move(game: Game):
    start_time = time.time()

    _, move = minimax(game, DEPTH, ALPHA, BETA)
    print('Valittu siirto on ' + str(move))

    elapsed_time = time.time() - start_time
    print(f"Siirron laskemiseen kului {elapsed_time:.2f} sekuntia")

    # Varmistetaan, että tekoälyn siirroissa kestää vähintään sekunti
    if elapsed_time < 1:
        time.sleep(1 - elapsed_time)

    return move


def get_possible_moves(game: Game, maximizing_player: bool) -> List[Game]:
    possible_moves: List[Game] = []
    if game.is_in_initial_placement():
        for pasture in game.get_potential_initial_pastures():
            game.make_initial_turn(pasture)
            possible_moves.append(copy.deepcopy(game))
            game.undo_initial_move(pasture)
    else:
        for pasture in game.get_potential_sheep_to_move():
            for target_pasture in pasture.get_potential_targets(game.pastures):
                for sheep in range(1, pasture.get_amount_of_sheep()):
                    game.make_normal_turn(pasture, target_pasture, sheep)
                    possible_moves.append(copy.deepcopy(game))
                    game.undo_move(pasture, target_pasture, sheep)

    # Järjestetään mahdolliset siirrot heuristisen arvon mukaiseen paremmuusjärjestykseen
    return sorted(
        possible_moves, key=lambda move: move.evaluate_game_state(), reverse=maximizing_player)


def minimax(game: Game, depth: int, alpha: float, beta: float) -> Tuple[float, Game | None]:
    # Palautetaan pelitilanteen arvo, mikäli peli on ohi tai päästiin annettuun syvyyteen
    if depth == 0 or game.is_over_for_ai():
        return game.evaluate_game_state(), None

    maximizing_player = game.is_players_turn()
    possible_moves = get_possible_moves(game, maximizing_player)
    if not possible_moves:
        raise SystemError('No possible moves, but game not over')
    best_move: Game | None = None

    if maximizing_player:
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
