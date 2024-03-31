from typing import List
import pygame

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
INITIAL_SHEEP = 16


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


def render(screen, font, pastures: List[Pasture], chosen_pasture: Pasture, turn_number: int, player_in_turn: int):
    """Piirretään laitumet näytölle"""

    def highlight(pasture: Pasture) -> None:
        pasture.render_highlight(
            screen, border_colour=HIGHLIGHTED_PASTURE_BORDER_COLOR)

    screen.fill(BACKGROUND_COLOR)

    margin = 50
    turn_text = font.render(
        f"{'Pelaajan' if player_in_turn == HUMAN_PLAYER else 'Tekoälyn'} vuoro", True, BLACK)

    text_rect = turn_text.get_rect()
    text_rect.topright = (screen.get_rect().right - margin, margin)
    screen.blit(turn_text, text_rect)

    for pasture in pastures:
        pasture.render(screen, font)
        # Piirretään reunat laitumen päälle
        pygame.draw.polygon(screen, PASTURE_BORDER_COLOR,
                            pasture.vertices, PASTURE_BORDER_WIDTH)

    mouse_position = pygame.mouse.get_pos()
    for pasture in pastures:
        if pasture.collide_with_point(mouse_position):
            if is_sheep_placement(turn_number) and not pasture.is_taken() and pasture.is_on_edge(pastures):
                highlight(pasture)
            if not is_sheep_placement(turn_number) and pasture.is_taken() and pasture.owner == player_in_turn:
                highlight(pasture)
        elif pasture is chosen_pasture or pasture.targeted or pasture.planned_sheep is not None:
            highlight(pasture)

    pygame.display.flip()


def is_sheep_placement(turn):
    return turn < 3


def next_turn(player_in_turn):
    if player_in_turn == HUMAN_PLAYER:
        return COMPUTER_PLAYER
    return HUMAN_PLAYER


def remove_targets(pastures: List[Pasture]):
    for pasture in pastures:
        pasture.targeted = False


def place_sheep(player, pasture: Pasture, pastures: List[Pasture]) -> None:
    """Asetetaan lampaat laitumelle, mikäli säännöt sallivat"""
    if pasture.is_on_edge(pastures) and not pasture.is_taken():
        pasture.update_sheep(owner=player, new_amount=INITIAL_SHEEP)


def game_is_over(pastures, turn_number, player_in_turn) -> bool:
    if is_sheep_placement(turn_number):
        return False
    for pasture in pastures:
        if pasture.owner == player_in_turn and pasture.sheep > 1:
            potential_moves = pasture.get_potential_targets(pastures)
            if len(potential_moves) > 0:
                return False
    return True


def main():
    pygame.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    clock = pygame.time.Clock()

    running = True

    pastures = init_pastures()
    player_in_turn = HUMAN_PLAYER
    turn_number = 1
    chosen_pasture = None
    target_pasture = None

    # Pelin suoritus
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
                mouse_pos = pygame.mouse.get_pos()
                for pasture in pastures:
                    # Etsitään valittu laidun
                    if pasture.collide_with_point(mouse_pos):
                        if is_sheep_placement(turn_number):
                            if not pasture.is_taken():
                                place_sheep(player_in_turn, pasture, pastures)
                                turn_number += 1
                                player_in_turn = next_turn(player_in_turn)
                        else:  # Aloituslampaat on jo asetettu
                            if pasture.is_taken() and pasture.owner == player_in_turn and pasture.sheep > 1:
                                # Valitaan lähtöruutu
                                chosen_pasture = pasture
                                targets = pasture.get_potential_targets(
                                    pastures)
                                for target in targets:
                                    target.targeted = True
                            elif pasture.targeted and chosen_pasture is not None and pasture is not chosen_pasture:
                                # Jos lähtöruutu valittu, valitaan kohderuutu
                                target_pasture = pasture
                                pasture.planned_sheep = 1
                                chosen_pasture.planned_sheep = chosen_pasture.sheep - 1
            elif ((event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_UP) or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP)) and target_pasture is not None and chosen_pasture is not None:
                if chosen_pasture.planned_sheep > 1:
                    chosen_pasture.deduct_a_sheep()
                    target_pasture.add_a_sheep()
            elif ((event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_DOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN)) and target_pasture is not None and chosen_pasture is not None:
                if target_pasture.planned_sheep > 1:
                    target_pasture.deduct_a_sheep()
                    chosen_pasture.add_a_sheep()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if target_pasture is not None and target_pasture.planned_sheep > 0 and chosen_pasture is not None and chosen_pasture.planned_sheep > 0:
                    chosen_pasture.move_sheep_to(target_pasture)
                    remove_targets(pastures)
                    chosen_pasture = None
                    target_pasture = None
                    turn_number += 1
                    player_in_turn = next_turn(player_in_turn)

            for pasture in pastures:
                pasture.update()

            render(screen, font, pastures, chosen_pasture,
                   turn_number, player_in_turn)
            clock.tick(50)
            if game_is_over(pastures, turn_number, player_in_turn):
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
