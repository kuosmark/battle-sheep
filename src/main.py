import time
import pygame

from game import Game
from minimax import minimax

DISPLAY_SIZE = (960, 540)
FONT_SIZE = 48
PASTURE_BORDER_WIDTH = 4
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3
MOUSE_WHEEL_SCROLL_UP = 4
MOUSE_WHEEL_SCROLL_DOWN = 5

PASTURE_BORDER_COLOR = (90, 110, 2)  # tummempi ruoho
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def render(screen, font, game: Game):
    """Piirretään laitumet näytölle"""

    screen.fill(WHITE)
    margin = 50
    if game.is_over():
        text = font.render(
            f'{game.get_winner_text()}', True, BLACK)
    else:
        text = font.render(
            f"{'Pelaajan' if game.is_humans_turn else 'Tekoälyn'} vuoro", True, BLACK)

    text_rect = text.get_rect()
    text_rect.topright = (screen.get_rect().right - margin, margin)
    screen.blit(text, text_rect)

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


def is_left_button_pressed(event) -> bool:
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON


def is_right_button_or_enter_pressed(event) -> bool:
    """Palauttaa tosi, jos joko hiiren oikeaa painiketta tai Enter-näppäintä on painettu"""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN


def is_mouse_wheel_scrolled_up(event) -> bool:
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_UP:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_UP


def is_mouse_wheel_scrolled_down(event) -> bool:
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_DOWN:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN


def init_pygame():
    """Alustetaan Pygame"""
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    font = pygame.font.SysFont(None, FONT_SIZE)
    return screen, font


def main():
    screen, font = init_pygame()
    game = Game()

    while True:
        if game.is_humans_turn:
            # Pelaajan vuoro
            for event in pygame.event.get():
                if is_left_button_pressed(event):
                    game.click(pygame.mouse.get_pos())
                elif is_mouse_wheel_scrolled_up(event):
                    game.try_to_add_sheep_to_planned_move()
                elif is_mouse_wheel_scrolled_down(event):
                    game.try_to_subtract_sheep_from_planned_move()
                elif is_right_button_or_enter_pressed(event):
                    game.confirm_move()
        elif not game.is_humans_turn and not game.is_over_for_ai():
            # Tekoälyn vuoro.
            start_time = time.time()
            # Algoritmi vaatii vielä nopeuttamista, joten syvyys ei toistaiseksi ole suuri.
            _, new_game_state = minimax(
                game, 2, alpha=float('-Inf'), beta=float('Inf'))
            # Lasketaan siirtoon kulunut aika
            elapsed_time = time.time() - start_time
            print(f"Siirron laskemiseen kului {elapsed_time:.2f} sekuntia")
            print('Valittu siirto on ' + str(new_game_state))
            # Varmistetaan, että tekoälyn siirroissa kestää vähintään sekunti,
            # jotta pelaaja ehtii käsittää, mitä tapahtuu
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)
            game = new_game_state

        render(screen, font, game)


if __name__ == "__main__":
    main()
