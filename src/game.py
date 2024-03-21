import board

# Peli-tietorakenteeseen kuuluu pelilaudan tilanne ja
# seuraavana vuorossa olevan pelaajan tunniste
type Game = dict[board.Board, int]


def evaluate_game_state(game_state: Game) -> float:
    return 0.5
