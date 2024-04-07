from typing import List
import pygame

from game import Game
from pasture import Pasture


DISPLAY_SIZE = (960, 540)
FONT_SIZE = 48
PASTURE_BORDER_WIDTH = 4
LEFT_MOUSE_BUTTON = 1
MOUSE_WHEEL_SCROLL_UP = 4
MOUSE_WHEEL_SCROLL_DOWN = 5

PASTURE_BORDER_COLOR = (90, 110, 2)  # tummempi ruoho
HIGHLIGHTED_PASTURE_BORDER_COLOR = (0, 0, 0)  # musta
BACKGROUND_COLOR = (255, 255, 255)  # valkoinen
BLACK = (0, 0, 0)

HUMAN_PLAYER = 0
COMPUTER_PLAYER = 1


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


def render(screen, font, game: Game):
    """Piirretään laitumet näytölle"""

    def highlight(pasture: Pasture) -> None:
        pasture.render_highlight(
            screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)

    screen.fill(BACKGROUND_COLOR)

    margin = 50
    turn_text = font.render(
        f"{'Pelaajan' if game.is_humans_turn else 'Tekoälyn'} vuoro", True, BLACK)

    text_rect = turn_text.get_rect()
    text_rect.topright = (screen.get_rect().right - margin, margin)
    screen.blit(turn_text, text_rect)

    for pasture in game.pastures:
        pasture.render(screen, font)
        # Piirretään reunat laitumen päälle
        pygame.draw.polygon(screen, PASTURE_BORDER_COLOR,
                            pasture.vertices, PASTURE_BORDER_WIDTH)

    mouse_position = pygame.mouse.get_pos()
    for pasture in game.pastures:
        if pasture is game.chosen_pasture or pasture.targeted or pasture.planned_sheep is not None:
            highlight(pasture)
        elif pasture.collide_with_point(mouse_position):
            if game.is_in_initial_placement() and not pasture.is_taken() and pasture.is_on_edge(game.pastures):
                highlight(pasture)
            if not game.is_in_initial_placement() and pasture.is_taken() and game.is_controlled_by_player_in_turn(pasture):
                highlight(pasture)

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    running = True

    game = Game(init_pastures())

    # Pelin suoritus
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif not game.is_humans_turn:
                # Tekoälyn vuoro
                game.make_random_ai_move()
                game.next_turn()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
                mouse_pos = pygame.mouse.get_pos()
                for pasture in game.pastures:
                    # Etsitään valittu laidun
                    if pasture.collide_with_point(mouse_pos):
                        if game.is_in_initial_placement():
                            if pasture.is_on_edge(game.pastures) and not pasture.is_taken():
                                game.place_initial_sheep(pasture)
                                game.next_turn()
                        else:  # Aloituslampaat on jo asetettu
                            if pasture.is_taken() and game.is_controlled_by_player_in_turn(pasture):
                                # Valitaan lähtöruutu
                                game.chosen_pasture = pasture
                                targets = pasture.get_potential_targets(
                                    game.pastures)
                                for target in targets:
                                    target.targeted = True
                            elif pasture.targeted and game.chosen_pasture is not None and pasture is not game.chosen_pasture:
                                # Jos lähtöruutu valittu, valitaan kohderuutu
                                game.target_pasture = pasture
                                pasture.planned_sheep = 1
                                game.chosen_pasture.planned_sheep = game.chosen_pasture.sheep - 1
            elif ((event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_UP) or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP)) and game.target_pasture is not None and game.chosen_pasture is not None:
                game.try_to_add_sheep_to_planned_move()
            elif ((event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_DOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN)) and game.target_pasture is not None and game.chosen_pasture is not None:
                game.try_to_subtract_sheep_from_planned_move()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if game.target_pasture is not None and game.target_pasture.planned_sheep > 0 and game.chosen_pasture is not None and game.chosen_pasture.planned_sheep > 0:
                    game.chosen_pasture.move_sheep_to(game.target_pasture)
                    game.next_turn()

            for pasture in game.pastures:
                pasture.update()

            render(screen, font, game)
            clock.tick(50)
            if game.is_over():
                screen.fill(BLACK)
                text = font.render('Peli on ohi! Pisteet: 1000', True, 'white')
                text_rect = text.get_rect(
                    center=(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

    pygame.display.quit()


if __name__ == "__main__":
    main()
