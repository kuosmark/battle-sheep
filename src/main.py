from typing import List
import pygame

from pasture import Pasture


DISPLAY_SIZE = (960, 540)
FONT_SIZE = 48

PASTURE_BORDER_COLOR = (90, 110, 2)  # tummempi ruoho
HIGHLIGHTED_PASTURE_BORDER_COLOR = (0, 0, 0)  # musta
BACKGROUND_COLOR = (255, 255, 255)  # valkoinen


def init_pastures(x_length=8, y_length=4) -> List[Pasture]:
    """Luodaan heksagonilaitumista pelilauta"""
    initial_position = (50, 50)
    leftmost_pasture = Pasture(initial_position)
    pastures = [leftmost_pasture]

    for y_axis in range(y_length):
        if y_axis > 0:
            position = leftmost_pasture.vertices[2]
            leftmost_pasture = Pasture(position)
            pastures.append(leftmost_pasture)

        pasture = leftmost_pasture
        for x_axis in range(x_length - 1):
            (x, y) = pasture.position
            # Piirretään joka toinen laidun ylä- ja joka toinen alaviistoon edellisestä
            if x_axis % 2 == 1:
                position = (x + pasture.radius * 3 / 2,
                            y - pasture.minimal_radius)
            else:
                position = (x + pasture.radius * 3 / 2,
                            y + pasture.minimal_radius)
            pasture = Pasture(position)
            pastures.append(pasture)

    return pastures


def render(screen, font, pastures):
    """Piirretään laitumet näytölle"""
    screen.fill(BACKGROUND_COLOR)
    border_width = 4

    for pasture in pastures:
        pasture.render(screen, font)
        # Piirretään reunat laitumen päälle
        pygame.draw.polygon(screen, PASTURE_BORDER_COLOR,
                            pasture.vertices, border_width)

    # Valaistaan hiiren osoittama laidun sekä sen viereiset laitumet
    # TODO: Valaistaan jatkossa pelaajan sallitut siirrot
    mouse_position = pygame.mouse.get_pos()
    for pasture in pastures:
        if pasture.collide_with_point(mouse_position):
            for neighbour in pasture.compute_neighbours(pastures):
                neighbour.render_highlight(
                    screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)
            pasture.render_highlight(
                screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)
    pygame.display.flip()


def main():
    pygame.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    clock = pygame.time.Clock()

    pastures = init_pastures()
    running = True

    # Pelin suoritus
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for pasture in pastures:
                    # Etsitään valittu laidun
                    if pasture.collide_with_point(mouse_pos):
                        # Asetetaan lampaita
                        pasture.update_sheep(16)

        for pasture in pastures:
            pasture.update()

        render(screen, font, pastures)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
