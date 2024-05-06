from typing import List

from constants import (
    INITIAL_POSITION,
    MINIMAL_RADIUS,
    PASTURE_RADIUS
)
from pasture import Pasture


def init_pastures(board_height: int, board_width: int) -> List[Pasture]:
    """Luodaan pelilaudan laitumet"""
    leftmost_pasture = Pasture(INITIAL_POSITION)
    pastures = [leftmost_pasture]

    for y_axis in range(board_height):
        if y_axis > 0:
            position = leftmost_pasture.vertices[2]
            leftmost_pasture = Pasture(position)
            pastures.append(leftmost_pasture)

        pasture = leftmost_pasture
        for x_axis in range(board_width - 1):
            (x, y) = pasture.position
            # Lisätään joka toinen laidun ylä- ja joka toinen alaviistoon edellisestä
            if x_axis % 2 == 1:
                position = (x + PASTURE_RADIUS * 3 / 2,
                            y - MINIMAL_RADIUS)
            else:
                position = (x + PASTURE_RADIUS * 3 / 2,
                            y + MINIMAL_RADIUS)
            pasture = Pasture(position)
            pastures.append(pasture)

    return pastures


def calculate_initial_sheep(board_height: int, board_width: int) -> int:
    amount_of_pastures = board_height * board_width
    if amount_of_pastures % 2 != 0:
        raise ValueError('Invalid board dimensions')
    return int(amount_of_pastures / 2)
