
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
    COMPUTERS_PASTURE_COLOR,
    DEPTH,
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
        self.is_running = False
        pygame.quit()

    def _get_pasture_in_mouse_position(self) -> Pasture | None:
        position = pygame.mouse.get_pos()
        for pasture in self._game.pastures:
            if pasture.collide_with_point(position):
                return pasture
        return None

    def _handle_input(self, event):
        """Käsitellään pelaajan syötteet"""
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
        """Lisätään teksti määriteltyyn kohtaan"""
        text_surface = self._sidebar_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(
            top=top, right=self._screen.get_rect().right - SIDEBAR_MARGIN)

        self._screen.blit(text_surface, text_rect)
        # Palautetaan seuraavan tekstin asema
        return text_rect.bottom + 10

    def _get_player_in_turn_text(self) -> str:
        if self._game.is_players_turn:
            return 'Pelaaja'
        return 'Tekoäly'

    def _get_winner_text(self) -> str:
        winner = self._game.calculate_winner()
        if winner == PLAYER:
            return 'Pelaaja on voittanut!'
        if winner == COMPUTER:
            return 'Tekoäly on voittanut!'
        return 'Tasapeli'

    def _get_largest_herd_text(self) -> str:
        largest_herd_owner = self._game.calculate_who_has_largest_herd()
        if largest_herd_owner == PLAYER:
            return f'Pelaaja, {self._game.get_players_largest_herd()}'
        computers_largest_herd = self._game.get_computers_largest_herd()
        if largest_herd_owner == COMPUTER:
            return f'Tekoäly, {computers_largest_herd}'
        return f'Tasapeli, {computers_largest_herd}'

    def _render_sidebar(self):
        """Piirretään lisätietosarake näytölle"""
        top_margin = self._render_sidebar_text(
            self._get_player_in_turn_text(), SIDEBAR_MARGIN)

        top_margin = self._render_sidebar_text(
            f'Vuoro: {self._game.get_number_of_turn()}', top_margin)

        top_margin = self._render_sidebar_text(
            f'Vaikeustaso: {DEPTH}', top_margin)

        top_margin = self._render_sidebar_text(
            f'Tilanne: {self._game.latest_value}', top_margin)

        top_margin = self._render_sidebar_text(
            f'Siirron kesto: {self._game.latest_computation_time:.2f}s', top_margin)

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
        """Palauttaa laitumen värin miehittäjän ja fokuksen perusteella"""
        color = FREE_PASTURE_COLOR

        if pasture.is_occupied_by_player():
            color = PLAYERS_PASTURE_COLOR
        if pasture.is_occupied_by_computer():
            color = COMPUTERS_PASTURE_COLOR

        if self._game.is_focused(pasture, pasture.collide_with_point(mouse)):
            return tuple(x + HIGHLIGHT_OFFSET if x + HIGHLIGHT_OFFSET < 255 else 255 for x in color)

        return color

    def _render_pasture(self, pasture: Pasture, mouse_position: Tuple[int, int]):
        """Piirretään laidun näytölle"""
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
        self._screen.fill(WHITE)
        mouse_position = pygame.mouse.get_pos()
        for pasture in self._game.pastures:
            self._render_pasture(pasture, mouse_position)

    def _render(self):
        self._render_board()
        self._render_sidebar()
        pygame.display.flip()
        self._clock.tick(60)

    # Pelin suoritus

    def _update_game_state(self):
        start_time = time.time()
        _, next_game_state = minimax(
            self._game, self._game.get_depth(), ALPHA, BETA, self._game.is_players_turn)

        elapsed_time = time.time() - start_time

        # Varmistetaan, että siirrossa kestää vähintään sekunti
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)

        if next_game_state is None:
            raise SystemError('No next move found')

        self._game = next_game_state
        self._game.latest_value = next_game_state.evaluate_game_state()
        self._game.latest_computation_time = elapsed_time

    def play_game(self) -> None:
        if self._game.is_next_move_calculated():
            self._update_game_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()

            if self._game.is_input_allowed():
                self._handle_input(event)

        self._render()
