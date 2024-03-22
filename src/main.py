from typing import List
from typing import Tuple

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile


PASTURE_COLOR = (163, 178, 3)  # vaalea ruoho
PASTURE_BORDER_COLOR = (90, 110, 2)  # tummempi ruoho
HIGHLIGHTED_PASTURE_BORDER_COLOR = (0, 0, 0)  # musta
BACKGROUND_COLOR = (255, 255, 255)  # valkoinen


def create_hexagon(position, radius=50, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=PASTURE_COLOR)


def init_hexagons(num_x=8, num_y=4, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    leftmost_hexagon = create_hexagon(position=(50, 50), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2,
                                y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2,
                                y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    return hexagons


def render(screen, font, hexagons):
    """Renders hexagons on the screen with visible borders"""
    screen.fill(BACKGROUND_COLOR)
    border_width = 4

    for hexagon in hexagons:
        hexagon.render(screen, font)
        # Renders the hexagon fill
        # Now draw the border over the filled hexagon
        pygame.draw.polygon(screen, PASTURE_BORDER_COLOR,
                            hexagon.vertices, border_width)

    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        for neighbour in hexagon.compute_neighbours(hexagons):
            neighbour.render_highlight(
                screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)
        hexagon.render_highlight(
            screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)
    pygame.display.flip()


DISPLAY_SIZE = (960, 540)


def main():
    pygame.init()
    font = pygame.font.SysFont(None, 48)

    screen = pygame.display.set_mode(DISPLAY_SIZE)
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=True)
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for hexagon in hexagons:
                    # Etsitään valittu laidun
                    if hexagon.collide_with_point(mouse_pos):
                        # Lampaiden asetus
                        hexagon.update_sheep(16)

        for hexagon in hexagons:
            hexagon.update()

        render(screen, font, hexagons)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
