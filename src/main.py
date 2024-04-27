import sys
import time
from typing import Tuple
import pygame
from constants import ALPHA, BETA, BLACK, BOARD_FONT_SIZE, DEPTH, DISPLAY_SIZE, LEFT_MOUSE_BUTTON, MOUSE_WHEEL_SCROLL_DOWN, MOUSE_WHEEL_SCROLL_UP, RIGHT_MOUSE_BUTTON, SIDEBAR_FONT_SIZE, SIDEBAR_MARGIN, SIMULATION_DEPTH, WHITE
from game import Game
from minimax import minimax


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


def render_text(screen, font, text, top) -> int:
    """Lisätään teksti määriteltyyn kohtaan"""
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(
        top=top, right=screen.get_rect().right - SIDEBAR_MARGIN)
    screen.blit(text_surface, text_rect)
    # Palautetaan seuraavan tekstin asema
    return text_rect.bottom + 10


def render_sidebar(screen, font, game, game_value, computation_time):
    """Piirretään lisätietosarake ruudulle"""
    player_in_turn_text = game.get_player_in_turn_text()
    top_margin = render_text(screen, font,
                             player_in_turn_text, SIDEBAR_MARGIN)

    turn_number_text = f'Vuoro: {game.get_number_of_turn()}'
    top_margin = render_text(screen, font,
                             turn_number_text, top_margin)

    difficulty_level_text = f'Vaikeustaso: {DEPTH}'
    top_margin = render_text(screen, font,
                             difficulty_level_text, top_margin)

    game_value_text = f'Tilanne: {game_value:.2f}'
    top_margin = render_text(screen, font,
                             game_value_text, top_margin)

    computation_time_text = f'Siirron kesto: {
        computation_time:.2f}s'
    top_margin = render_text(screen, font,
                             computation_time_text, top_margin)


def render_board(screen, font, game):
    screen.fill(WHITE)
    mouse_position = pygame.mouse.get_pos()
    for pasture in game.pastures:
        game.adjust_focus(pasture, mouse_position)
        pasture.render(screen, font)


def compute_next_turn(game: Game, is_simulation: bool) -> Tuple[Game, float, float]:
    depth = SIMULATION_DEPTH if is_simulation else DEPTH
    start_time = time.time()

    next_value, next_game_state = minimax(game, depth, ALPHA, BETA)
    if next_game_state is None:
        raise SystemError('Game state calculation failed')

    elapsed_time = time.time() - start_time

    # Varmistetaan, että siirrossa kestää vähintään sekunti
    if elapsed_time < 1:
        time.sleep(1 - elapsed_time)
    return next_game_state, next_value, elapsed_time


def init_pygame():
    """Alustetaan Pygame"""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    board_font = pygame.font.SysFont(None, BOARD_FONT_SIZE, False, True)
    sidebar_font = pygame.font.SysFont(None, SIDEBAR_FONT_SIZE)
    return clock, screen, board_font, sidebar_font


def init_variables() -> Tuple[Game, float, float, True]:
    """Alustetaan muuttujat"""
    return Game(), 0, 0, True


def main(is_simulation: bool):
    clock, screen, board_font, sidebar_font = init_pygame()
    game, game_value, latest_computation_time, running = init_variables()

    while running:
        if game.is_computers_turn() and not game.is_over_for_computer():
            game, game_value, latest_computation_time = compute_next_turn(
                game, is_simulation)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game.is_players_turn():
                if is_simulation:
                    game, game_value, latest_computation_time = compute_next_turn(
                        game, is_simulation)
                else:
                    handle_event(game, event)

        render_board(screen, board_font, game)
        render_sidebar(screen, sidebar_font, game,
                       game_value, latest_computation_time)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ai':
        main(is_simulation=True)

    main(is_simulation=False)
