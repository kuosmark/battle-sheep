type Occupancy = tuple[int, int] | None  # Pelaajan tunniste ja lampaiden määrä
type Cell = tuple[int, int, int]  # Ruudun koordinaatit
type Board = dict[Cell, Occupancy]

# Pelilauta, jossa akselien Q, R ja S koordinaatit
board: Board = {
    (-4, 1, 3), (-4, 4, 0),
    (-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0), (-3, 4, -1),
    (-2, 0, 2), (-2, 1, 1), (-2, 2, 0), (-2, 3, -1),
    (-1, 0, 1), (-1, 1, 0), (-1, 2, -1),
    (0, -1, 1), (0, 0, 0), (0, 1, -1), (0, 2, -2),
    (1, -1, 0), (1, 0, -1), (1, 1, -2),
    (2, -2, 0), (2, -1, -1), (2, 0, -2), (2, 1, -3),
    (3, -3, 0), (3, -2, -1), (3, -1, -2), (3, 0, -3), (3, 1, -4),
    (4, -3, -1), (4, 0, -4)
}


def place_sheep(player_id: int, amount: int, position: Cell):
    if (0 <= position[0] < WIDTH) and (0 <= position[1] < HEIGHT) and (0 < amount <= 16):
        print(position)
        occupancy: Occupancy = board.get(position, None)
        if occupancy is None:
            board[position] = (player_id, amount)
            print('Onnistui!')
        else:
            print('Ruutu on jo varattu, kokeile uudelleen!')
    else:
        print('Virheelliset arvot, kokeile uudelleen!')


def display():
    for row in range(HEIGHT):
        row_output: list[str] = []
        for col in range(WIDTH):
            value = board.get((col, row), None)
            if value is None:
                row_output.append('0')
            else:
                row_output.append(str(value[1]))
        print(' '.join(row_output))
