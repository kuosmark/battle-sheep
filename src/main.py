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


def get_event_name(event) -> str:
    return pygame.event.event_name(event.type)


def is_left_button_pressed(event) -> bool:
    return get_event_name(event) == 'MouseButtonDown' and event.button == LEFT_MOUSE_BUTTON


def is_mouse_wheel_scrolled_up(event) -> bool:
    if get_event_name(event) == 'MouseButtonDown' and event.button == MOUSE_WHEEL_SCROLL_UP:
        return True
    if get_event_name(event) == 'KeyDown' and event.key == pygame.K_UP:
        return True
    return False


def is_mouse_wheel_scrolled_down(event) -> bool:
    if get_event_name(event) == 'MouseButtonDown' and event.button == MOUSE_WHEEL_SCROLL_DOWN:
        return True
    if get_event_name(event) == 'KeyDown' and event.key == pygame.K_DOWN:
        return True
    return False


def is_enter_pressed(event) -> bool:
    return get_event_name(event) == 'KeyDown' and event.key == pygame.K_RETURN


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    running = True

    game = Game()

    # Pelin suoritus
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game.is_humans_turn:
                # Tekoälyn vuoro
                game.make_ai_move()
                clock.tick(50)
            elif is_left_button_pressed(event):
                mouse_pos = pygame.mouse.get_pos()
                for pasture in game.pastures:
                    # Etsitään valittu laidun
                    if pasture.collide_with_point(mouse_pos):
                        game.click_on_pasture(pasture)
            elif is_mouse_wheel_scrolled_up(event) and game.are_pastures_chosen():
                game.try_to_add_sheep_to_planned_move()
            elif is_mouse_wheel_scrolled_down(event) and game.are_pastures_chosen():
                game.try_to_subtract_sheep_from_planned_move()
            elif is_enter_pressed(event):
                game.confirm_move()

            for pasture in game.pastures:
                pasture.update()

            render(screen, font, game)
            if game.is_over():
                screen.fill(BLACK)
                winner = game.calculate_winner()
                text = font.render(
                    f'{winner}', True, 'white')
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
