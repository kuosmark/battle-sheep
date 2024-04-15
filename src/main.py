import pygame

from game import Game
from minimax import calculate_ai_move

DISPLAY_SIZE = (960, 540)
FONT_SIZE = 48
PASTURE_BORDER_WIDTH = 4
LEFT_MOUSE_BUTTON = 1
MOUSE_WHEEL_SCROLL_UP = 4
MOUSE_WHEEL_SCROLL_DOWN = 5

PASTURE_BORDER_COLOR = (90, 110, 2)  # tummempi ruoho
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def render(screen: pygame.Surface, font: pygame.Font, game: Game):
    """Piirretään laitumet näytölle"""

    if game.is_over():
        screen.fill(BLACK)
        winner = game.get_winner_text()
        text = font.render(
            f'{winner}', True, 'white')
        text_rect = text.get_rect(
            center=(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2))
        screen.blit(text, text_rect)
    else:
        screen.fill(WHITE)

        margin = 50
        turn_text = font.render(
            f"{'Pelaajan' if game.is_humans_turn else 'Tekoälyn'} vuoro", True, BLACK)

        text_rect = turn_text.get_rect()
        text_rect.topright = (screen.get_rect().right - margin, margin)
        screen.blit(turn_text, text_rect)

        mouse_position = pygame.mouse.get_pos()
        for pasture in game.pastures:
            pointed_at = pasture.collide_with_point(mouse_position)
            # Fokusoidut laitumet merkitään vaaleammalla taustavärillä
            pasture.focused = game.should_be_focused(
                pasture, pointed_at)
            pasture.render(screen, font)
            # Piirretään reunat laitumen päälle
            pygame.draw.polygon(screen, PASTURE_BORDER_COLOR,
                                pasture.vertices, PASTURE_BORDER_WIDTH)

    pygame.display.flip()


def get_event_name(event: pygame.Event) -> str:
    return pygame.event.event_name(event.type)


def is_left_button_pressed(event: pygame.Event) -> bool:
    return get_event_name(event) == 'MouseButtonDown' and event.button == LEFT_MOUSE_BUTTON


def is_mouse_wheel_scrolled_up(event: pygame.Event) -> bool:
    if get_event_name(event) == 'MouseButtonDown' and event.button == MOUSE_WHEEL_SCROLL_UP:
        return True
    if get_event_name(event) == 'KeyDown' and event.key == pygame.K_UP:
        return True
    return False


def is_mouse_wheel_scrolled_down(event: pygame.Event) -> bool:
    if get_event_name(event) == 'MouseButtonDown' and event.button == MOUSE_WHEEL_SCROLL_DOWN:
        return True
    if get_event_name(event) == 'KeyDown' and event.key == pygame.K_DOWN:
        return True
    return False


def is_enter_pressed(event: pygame.Event) -> bool:
    return get_event_name(event) == 'KeyDown' and event.key == pygame.K_RETURN


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    font = pygame.font.SysFont(None, FONT_SIZE)

    game = Game()
    running = True

    while running:
        if game.is_humans_turn:
            # Pelaajan vuoro
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif is_left_button_pressed(event):
                    mouse_pos = pygame.mouse.get_pos()
                    for pasture in game.pastures:
                        # Etsitään valittu laidun
                        if pasture.collide_with_point(mouse_pos):
                            game.click_on_pasture(pasture)
                elif is_mouse_wheel_scrolled_up(event):
                    game.try_to_add_sheep_to_planned_move()
                elif is_mouse_wheel_scrolled_down(event):
                    game.try_to_subtract_sheep_from_planned_move()
                elif is_enter_pressed(event):
                    game.confirm_move()
        else:
            if not game.is_over_for_ai:
                # Tekoälyn vuoro
                pygame.time.wait(1000)
                next_pasture, next_target, sheep = calculate_ai_move(
                    game)
                game.make_ai_move(next_pasture, next_target, sheep)

        render(screen, font, game)

    pygame.display.quit()


if __name__ == "__main__":
    main()
