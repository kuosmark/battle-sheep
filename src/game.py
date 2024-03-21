import board

# Peli-tietorakenteeseen kuuluu pelilaudan tilanne ja
# seuraavana vuorossa olevan pelaajan tunniste
type game = dict[board.Board, int]


def evaluate_game_state(game_state):
    return 0.5
