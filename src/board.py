WIDTH = 4  # x-akseli
HEIGHT = 8  # y-akseli

type Occupancy = tuple[int, int] | None  # Pelaajan tunniste ja lampaiden määrä
type Cell = tuple[int, int]  # Ruudun koordinaatit
type Board = dict[Cell, Occupancy]

# Alustetaan laudan jokaisen ruudun arvoksi None.
board: Board = {(x, y): None for x in range(WIDTH)
                for y in range(HEIGHT)}


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
