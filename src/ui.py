
import time
from typing import Tuple
import pygame
from constants import (
    ALPHA,
    BETA,
    BLACK,
    BOARD_FONT_SIZE,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    COMPUTER,
    COMPUTER_DEPTH,
    COMPUTERS_PASTURE_COLOR,
    DISPLAY_SIZE,
    FREE_PASTURE_COLOR,
    HIGHLIGHT_OFFSET,
    LEFT_MOUSE_BUTTON,
    MOUSE_WHEEL_SCROLL_DOWN,
    MOUSE_WHEEL_SCROLL_UP,
    PASTURE_BORDER_COLOR,
    PASTURE_BORDER_WIDTH,
    PLAYER,
    PLAYERS_PASTURE_COLOR,
    RIGHT_MOUSE_BUTTON,
    SIDEBAR_DIVIDER,
    SIDEBAR_FONT_SIZE,
    SIDEBAR_MARGIN,
    SIMULATED_PLAYER_DEPTH,
    WHITE
)
from game import Game
from minimax import minimax
from pasture import Pasture


class Ui:
    def __init__(self, is_simulation: bool) -> None:
        pygame.init()
        self.is_running = True
        self._game = Game(BOARD_HEIGHT, BOARD_WIDTH, is_simulation)
        self._latest_game_value: float = 0
        self._latest_computation_time: float = 0
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(DISPLAY_SIZE)
        self._board_font = pygame.font.SysFont(
            'freesansbold', BOARD_FONT_SIZE, False, True)
        self._sidebar_font = pygame.font.SysFont(
            'freesansbold', SIDEBAR_FONT_SIZE)

    # Syötteet

    def _is_left_button_pressed(self, event) -> bool:
        """Palauttaa tosi, jos hiiren vasenta painiketta on painettu"""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON

    def _is_right_button_or_enter_pressed(self, event) -> bool:
        """Palauttaa tosi, jos hiiren oikeaa painiketta tai Enter-näppäintä on painettu"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
            return True
        return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN

    def _is_mouse_wheel_scrolled_up(self, event) -> bool:
        """Palauttaa tosi, jos hiiren rullaa on kelattu ylöspäin"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_UP:
            return True
        return event.type == pygame.KEYDOWN and event.key == pygame.K_UP

    def _is_mouse_wheel_scrolled_down(self, event) -> bool:
        """Palauttaa tosi, jos hiiren rullaa on kelattu alaspäin"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_WHEEL_SCROLL_DOWN:
            return True
        return event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN

    # Käyttöliittymätapahtumat

    def _exit(self):
        """Sulkee pelin"""
        self.is_running = False
        pygame.quit()

    def _get_pasture_in_mouse_position(self) -> Pasture | None:
        """Palauttaa hiiren osoittimen sijainnista laitumen, jos sellainen löytyy"""
        position = pygame.mouse.get_pos()
        for pasture in self._game.pastures:
            if pasture.collide_with_point(position):
                return pasture
        return None

    def _handle_input(self, event):
        """Käsittelee pelaajan syötteet"""
        if self._is_left_button_pressed(event):
            self._game.click_on_pasture(self._get_pasture_in_mouse_position())
        elif self._is_right_button_or_enter_pressed(event):
            self._game.press_enter()
        elif self._is_mouse_wheel_scrolled_up(event):
            self._game.scroll_up()
        elif self._is_mouse_wheel_scrolled_down(event):
            self._game.scroll_down()

    # Näyttö

    def _render_sidebar_text(self, text: str, top: int) -> int:
        """Lisää tekstin määriteltyyn kohtaan näytöllä"""
        text_surface = self._sidebar_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(
            top=top, right=self._screen.get_rect().right - SIDEBAR_MARGIN)

        self._screen.blit(text_surface, text_rect)
        # Palautetaan seuraavan tekstin asema
        return text_rect.bottom + 10

    def _get_player_in_turn_text(self) -> str:
        """Palauttaa tekstin vuorossa olevasta ottelijasta"""
        if self._game.is_players_turn:
            return 'Pelaaja'
        return 'Tekoäly'

    def _get_winner_text(self) -> str:
        """Palauttaa tekstin pelin voittajasta"""
        winner = self._game.calculate_winner()
        if winner == PLAYER:
            return 'Pelaaja on voittanut!'
        if winner == COMPUTER:
            return 'Tekoäly on voittanut!'
        return 'Tasapeli'

    def _get_largest_herd_text(self) -> str:
        """Palauttaa tekstin suurimman yhtenäisen alueen hallitsijasta"""
        largest_herd_owner = self._game.calculate_who_has_largest_herd()
        if largest_herd_owner == PLAYER:
            return f'Pelaaja, {self._game.get_players_largest_herd()}'
        computers_largest_herd = self._game.get_computers_largest_herd()
        if largest_herd_owner == COMPUTER:
            return f'Tekoäly, {computers_largest_herd}'
        return f'Tasapeli, {computers_largest_herd}'

    def _render_sidebar(self):
        """Lisää tietosarakkeen näytön oikeaan reunaan"""
        top_margin = self._render_sidebar_text(
            self._get_player_in_turn_text(), SIDEBAR_MARGIN)

        top_margin = self._render_sidebar_text(
            f'Vuoro: {self._game.get_number_of_turn()}', top_margin)

        top_margin = self._render_sidebar_text(
            f'Vaikeustaso: {COMPUTER_DEPTH, }', top_margin)

        top_margin = self._render_sidebar_text(
            f'Tilanne: {self._latest_game_value}', top_margin)

        top_margin = self._render_sidebar_text(
            f'Siirron kesto: {self._latest_computation_time:.2f}s', top_margin)

        if self._game.is_over():
            top_margin = self._render_sidebar_text(
                self._get_winner_text(), top_margin + SIDEBAR_DIVIDER)

            top_margin = self._render_sidebar_text(
                f'Pelaajan laitumet: {
                    self._game.get_amount_of_pastures_occupied_by_player()}',
                top_margin)

            top_margin = self._render_sidebar_text(
                f'Tekoälyn laitumet: {
                    self._game.get_amount_of_pastures_occupied_by_computer()}',
                top_margin)

            if self._game.is_equal_amount_of_pastures_occupied():
                self._render_sidebar_text(
                    f'Suurin alue: {self._get_largest_herd_text()}', top_margin)

    def _get_pasture_color(self, pasture: Pasture, mouse: Tuple[int, int]) -> Tuple[int, ...]:
        """Palauttaa laitumen värin miehittäjän ja valaisun perusteella"""
        color = FREE_PASTURE_COLOR

        if pasture.is_occupied_by_player():
            color = PLAYERS_PASTURE_COLOR
        if pasture.is_occupied_by_computer():
            color = COMPUTERS_PASTURE_COLOR

        if self._game.is_focused(pasture, pasture.collide_with_point(mouse)):
            return tuple(x + HIGHLIGHT_OFFSET if x + HIGHLIGHT_OFFSET < 255 else 255 for x in color)

        return color

    def _render_pasture(self, pasture: Pasture, mouse_position: Tuple[int, int]):
        """Lisää laitumen näytölle"""
        pasture_color = self._get_pasture_color(pasture, mouse_position)
        pygame.draw.polygon(self._screen, pasture_color, pasture.vertices)

        planned_sheep = pasture.get_amount_of_planned_sheep()
        sheep = pasture.get_amount_of_sheep()

        if planned_sheep > 0:
            text_surface = self._board_font.render(
                str(planned_sheep), True, BLACK)
            text_rect = text_surface.get_rect(center=pasture.centre)
            self._screen.blit(text_surface, text_rect)
        elif sheep > 0:
            text_surface = self._board_font.render(
                str(sheep), True, WHITE)
            text_rect = text_surface.get_rect(center=pasture.centre)
            self._screen.blit(text_surface, text_rect)

        # Piirretään laitumen reuna
        pygame.draw.polygon(self._screen, PASTURE_BORDER_COLOR,
                            pasture.vertices, PASTURE_BORDER_WIDTH)

    def _render_board(self):
        """Lisää pelilaudan laitumet näytölle"""
        self._screen.fill(WHITE)
        mouse_position = pygame.mouse.get_pos()
        for pasture in self._game.pastures:
            self._render_pasture(pasture, mouse_position)

    def _render(self):
        """Lisää pelilaudan ja lisätietosarakkeen näytölle"""
        self._render_board()
        self._render_sidebar()
        pygame.display.flip()
        self._clock.tick(60)

    # Pelin suoritus

    def _update_game_state(self):
        """Pelaa seuraavan vuoron minimaxia käyttäen"""
        start_time = time.time()

        depth = (SIMULATED_PLAYER_DEPTH if (self._game.is_simulation and self._game.is_players_turn)
                 else COMPUTER_DEPTH)
        _, next_game_state = minimax(
            self._game, depth, ALPHA, BETA, self._game.is_players_turn)

        if next_game_state is None:
            raise SystemError('No next move found')
        self._game = next_game_state

        elapsed_time = time.time() - start_time
        self._latest_computation_time = elapsed_time

        # Varmistetaan, että siirrossa kestää vähintään sekunti
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)

    def _update_latest_game_value(self) -> None:
        """Päivittää pelitilanteen arvon instanssimuuttujaan"""
        self._latest_game_value = self._game.evaluate_game_state()

    def play_game(self) -> None:
        """"Käsittelee pelitapahtumat"""
        if self._game.is_next_move_calculated():
            self._update_game_state()
            self._update_latest_game_value()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()

            if self._game.is_input_allowed():
                self._handle_input(event)
                self._update_latest_game_value()

        self._render()
