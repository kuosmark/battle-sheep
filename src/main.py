import pygame
from constants import BLACK, DISPLAY_SIZE, FONT_SIZE, LEFT_MOUSE_BUTTON, MOUSE_WHEEL_SCROLL_DOWN, MOUSE_WHEEL_SCROLL_UP, RIGHT_MOUSE_BUTTON, SIDEBAR_MARGIN, WHITE
from game import Game
from minimax import get_computers_move


def render(screen, font, game: Game):
    """Päivitetään käyttöliittymää"""
    screen.fill(WHITE)

    # Piirretään pelitiedot
    info_text = font.render(game.get_info_text(), True, BLACK)
    rect = info_text.get_rect(
        topright=(screen.get_rect().right - SIDEBAR_MARGIN, SIDEBAR_MARGIN))
    screen.blit(info_text, rect)

    # Piirretään laitumet
    mouse_position = pygame.mouse.get_pos()
    for pasture in game.pastures:
        game.adjust_focus(pasture, mouse_position)
        pasture.render(screen, font)

    pygame.display.flip()


def is_left_button_pressed(event) -> bool:
    """Palauttaa tosi, jos hiiren vasenta painiketta on painettu"""
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON


def is_right_button_or_enter_pressed(event) -> bool:
    """Palauttaa tosi, jos hiiren oikeaa painiketta tai Enter-näppäintä on painettu"""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN


def is_mouse_wheel_scrolled_up(event) -> bool:
    """Palauttaa tosi, jos hiiren rullaa on kelattu ylöspäin"""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_UP:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_UP


def is_mouse_wheel_scrolled_down(event) -> bool:
    """Palauttaa tosi, jos hiiren rullaa on kelattu alaspäin"""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_DOWN:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN


def init_pygame():
    """Alustetaan Pygame"""
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    font = pygame.font.SysFont(None, FONT_SIZE)
    return screen, font


def handle_event(game: Game, event):
    """Käsitellään pelaajan syötteet"""
    if is_left_button_pressed(event):
        game.click(pygame.mouse.get_pos())
    elif is_right_button_or_enter_pressed(event):
        game.press_enter()
    elif is_mouse_wheel_scrolled_up(event):
        game.scroll_up()
    elif is_mouse_wheel_scrolled_down(event):
        game.scroll_down()


def main():
    screen, font = init_pygame()
    game = Game()

    isSimulation = False

    while True:
        if isSimulation:
            while not game.is_over():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                game = get_computers_move(game)
                render(screen, font, game)

        if game.is_players_turn():
            for event in pygame.event.get():
                handle_event(game, event)
        elif game.is_computers_turn():
            game = get_computers_move(game)

        render(screen, font, game)


if __name__ == "__main__":
    main()
