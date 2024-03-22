from typing import Dict, List, Tuple

# Ruudun koordinaatit
type Cell = Tuple[int, int, int]

# Ruudun tilanne, arvoina ruudun vallanneen pelaajan tunniste ja lampaiden määrä
# None, jos ruutu on tyhjä
type Occupancy = Tuple[int, int] | None

# Pelilauta
type Board = Dict[Cell, Occupancy]

# Pelilaudan ruudut akselien Q, R ja S koordinaateilla ilmaistuna
cells: List[Cell] = [
    (-4, 1, 3), (-4, 4, 0),
    (-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0), (-3, 4, -1),
    (-2, 0, 2), (-2, 1, 1), (-2, 2, 0), (-2, 3, -1),
    (-1, 0, 1), (-1, 1, 0), (-1, 2, -1),
    (0, -1, 1), (0, 0, 0), (0, 1, -1), (0, 2, -2),
    (1, -1, 0), (1, 0, -1), (1, 1, -2),
    (2, -2, 0), (2, -1, -1), (2, 0, -2), (2, 1, -3),
    (3, -3, 0), (3, -2, -1), (3, -1, -2), (3, 0, -3), (3, 1, -4),
    (4, -3, -1), (4, 0, -4)
]

# Alustetaan laudan jokaisen ruudun arvoksi None.
board: Board = {cell: None for cell in cells}

MAX_SHEEP_AMOUNT = 16


def place_sheep(player_id: int, amount: int, position: Cell) -> None:
    if position in board and (0 < amount <= MAX_SHEEP_AMOUNT):
        occupancy = board.get(position, None)
        if occupancy is None:
            board[position] = (player_id, amount)
            print('Onnistui!')
        else:
            print('Ruutu on jo varattu, kokeile uudelleen!')
    else:
        print('Virheelliset arvot, kokeile uudelleen!')


def display() -> None:
    min_q = min(q for (q, r, s) in board.keys())
    max_q = max(q for (q, r, s) in board.keys())
    min_r = min(r for (q, r, s) in board.keys())
    max_r = max(r for (q, r, s) in board.keys())

    for q in range(min_q, max_q + 1):
        # Lisätään välilyönnit heksagonaalisuuden simuloimiseksi
        print(" " * abs(min_q - q), end="")
        for r in range(min_r, max_r + 1):
            s = - q - r
            if (q, r, s) in board:
                value = board.get((q, r, s), None)
                if value is None:
                    # Ellei lampaita ole, tulostetaan tyhjä ruutu
                    print('# ', end="")
                else:
                    # Tulostetaan lampaiden lukumäärä
                    print(f'{value[1]} ', end="")
            else:
                # Ellei ruutua ole pelilaudalla, tulostetaan "tyhjää tilaa"
                print('. ', end="")
        print()
