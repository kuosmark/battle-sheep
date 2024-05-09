import copy
from typing import List, Tuple
from game import Game


def get_possible_initial_moves(game: Game) -> List[Game]:
    possible_moves: List[Game] = []
    for pasture in game.get_potential_initial_pastures():
        game.make_initial_turn(pasture)
        possible_moves.append(copy.deepcopy(game))
        game.undo_initial_turn(pasture)
    return possible_moves


def get_possible_regular_moves(game: Game) -> List[Game]:
    possible_moves: List[Game] = []
    for pasture in game.get_potential_sheep_to_move_this_turn():
        for target_pasture in pasture.get_potential_targets(game.pastures):
            for sheep in range(1, pasture.get_amount_of_sheep()):
                game.make_normal_turn(pasture, target_pasture, sheep)
                possible_moves.append(copy.deepcopy(game))
                game.undo_normal_turn(pasture, target_pasture, sheep)
    return possible_moves


def get_possible_moves(game: Game, max_player: bool) -> List[Game]:
    """Palauttaa mahdolliset seuraavat siirrot järjestettynä heuristisen arvon mukaan"""
    possible_moves = (get_possible_initial_moves(game) if game.is_in_initial_placement()
                      else get_possible_regular_moves(game))

    return sorted(possible_moves,
                  key=lambda move: move.evaluate_game_state(),
                  reverse=max_player)


def is_unable_to_move(game: Game, max_player: bool) -> bool:
    if max_player:
        return game.is_over_for_player()
    return game.is_over_for_computer()


def minimax(game: Game, depth: int, alpha: float, beta: float, max_player: bool
            ) -> Tuple[float, Game | None]:
    # Palautetaan pelitilanteen arvo, mikäli päästiin annettuun syvyyteen
    # tai peli on ohi vuorossa olevalta pelaajalta
    if depth == 0 or is_unable_to_move(game, max_player):
        return game.evaluate_game_state(), None

    possible_moves: List[Game] = get_possible_moves(game, max_player)
    best_move: Game | None = None

    if max_player:
        best_value = float('-inf')
        for move in possible_moves:
            value, _ = minimax(move, depth - 1, alpha, beta, False)
            if value >= best_value:
                best_value = value
                best_move = move

            if best_value >= beta:
                break
            alpha = max(alpha, best_value)
    else:
        best_value = float('inf')
        for move in possible_moves:
            value, _ = minimax(move, depth - 1, alpha, beta, True)
            if value <= best_value:
                best_value = value
                best_move = move

            if best_value <= alpha:
                break
            beta = min(beta, best_value)

    return best_value, best_move
