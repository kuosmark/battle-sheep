import game


def get_next_moves(game_state):
    return []

# Minimax-algoritmi
# Muuttuja game_state sisältää laudan pelitilanteen, lampaiden sijainnit ja määrät.
# Muuttuja depth on syvyys, johon saakka pelitilanteet käydään läpi.
# Muuttuja is_max_player kertoo, onko heuristisen funktion arvon maksimoijan vuoro.


def minimax(game_state, depth: int, is_max_player: bool):
    if depth == 0:
        return game.evaluate_game_state(game_state)

    if is_max_player:  # Pelaaja tahtoo maksimoida arvon
        value = float('-Inf')  # Pelitilanteen heuristinen arvo
        next_moves = get_next_moves(game_state)
        for move in next_moves:
            value = max(value, minimax(move, depth - 1, False))
        return value

    # Pelaaja tahtoo minimoida arvon
    value = float('Inf')  # Pelitilanteen heuristinen arvo
    next_moves = get_next_moves(game_state)
    for move in next_moves:
        value = min(value, minimax(move, depth - 1, True))
    return value
