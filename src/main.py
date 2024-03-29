from typing import List
import pygame

from pasture import Pasture


DISPLAY_SIZE = (960, 540)
FONT_SIZE = 48
PASTURE_BORDER_WIDTH = 4

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


def render(screen, font, pastures, chosen_pasture, free_selection, player_in_turn):
    """Piirretään laitumet näytölle"""
    screen.fill(BACKGROUND_COLOR)

    for pasture in pastures:
        pasture.render(screen, font)
        # Piirretään reunat laitumen päälle
        pygame.draw.polygon(screen, PASTURE_BORDER_COLOR,
                            pasture.vertices, PASTURE_BORDER_WIDTH)

    # TODO: Valaistaan jatkossa pelaajan sallitut siirrot
    mouse_position = pygame.mouse.get_pos()
    for pasture in pastures:
        if pasture.collide_with_point(mouse_position):
            # for neighbour in pasture.compute_neighbours(pastures):
            #     neighbour.render_highlight(
            #         screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)
            if free_selection and pasture.is_on_edge(pastures) and not pasture.is_taken():
                pasture.render_highlight(
                    screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)
            if not free_selection and pasture.is_taken() and pasture.owner == player_in_turn:
                pasture.render_highlight(
                    screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)
        elif pasture is chosen_pasture or pasture.targeted:
            pasture.render_highlight(
                screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)

    pygame.display.flip()


def is_free_selection(turn):
    return turn < 3


def next_turn(player_in_turn):
    if player_in_turn == 0:
        return 1
    return 0


def remove_targets(pastures: List[Pasture]):
    for pasture in pastures:
        pasture.targeted = False


def game_is_over(pastures, turn_number, player_in_turn) -> bool:
    if turn_number < 4:
        return False
    potential_moves: int = 0
    for pasture in pastures:
        if pasture.owner == player_in_turn and pasture.sheep > 1:
            moves = pasture.get_potential_targets(pastures)
            potential_moves += len(moves)
    return potential_moves == 0


def main():
    pygame.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    clock = pygame.time.Clock()

    running = True

    pastures = init_pastures()
    player_in_turn = 0  # 0 = pelaaja, 1 = tekoäly
    turn_number = 1
    chosen_pasture = None

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
                        print('The centre of this pasture is at' +
                              str(pasture.centre))
                        if is_free_selection(turn_number):
                            # Asetetaan lampaat
                            if pasture.is_on_edge(pastures) and not pasture.is_taken():
                                pasture.update_sheep(
                                    owner=player_in_turn, new_amount=16)
                                turn_number += 1
                                player_in_turn = next_turn(player_in_turn)
                        else:
                            if pasture.is_taken() and pasture.owner == player_in_turn and pasture.sheep > 1:
                                chosen_pasture = pasture
                                targets = pasture.get_potential_targets(
                                    pastures)
                                for target in targets:
                                    target.targeted = True
                            elif pasture.targeted and chosen_pasture is not None:
                                remove_targets(pastures)
                                chosen_pasture.move_sheep_to(pasture)
                                chosen_pasture = None
                                turn_number += 1
                                player_in_turn = next_turn(player_in_turn)
            for pasture in pastures:
                pasture.update()

            render(screen, font, pastures, chosen_pasture,
                   is_free_selection(turn_number), player_in_turn)
            clock.tick(50)
            if game_is_over(pastures, turn_number, player_in_turn):
                score = 1000
                screen.fill('black')  # Clear the screen
                text = font.render(f'Peli on ohi! Pisteet: {
                                   score}', True, 'white')
                text_rect = text.get_rect(
                    center=(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2))
                screen.blit(text, text_rect)
                pygame.display.flip()  # Update the display
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

    pygame.display.quit()


if __name__ == "__main__":
    main()
