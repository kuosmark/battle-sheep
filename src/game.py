from typing import List
from constants import (
    COMPUTER,
    DEPTH,
    PLAYER,
    SIMULATED_PLAYER_DEPTH
)
from pasture import Pasture
from utils import calculate_initial_sheep, init_pastures


class Game:
    def __init__(self, board_height: int, board_width: int, is_simulation: bool) -> None:
        self.pastures: List[Pasture] = init_pastures(board_height, board_width)
        self.initial_sheep: int = calculate_initial_sheep(
            board_height, board_width)
        self._is_simulation = is_simulation
        self._turn: int = 1
        self.is_players_turn = True
        self._winner: int | None = None
        self.chosen_pasture: Pasture | None = None
        self.target_pasture: Pasture | None = None
        self.latest_value: float = 0
        self.latest_computation_time: float = 0

    # Syötteet

    def click_on_pasture(self, pasture: Pasture | None) -> None:
        if self.is_in_initial_placement(
        ) and pasture and pasture.is_potential_initial_pasture(self.pastures):
            self.make_initial_turn(pasture)
            self.latest_value = self.evaluate_game_state()
        elif pasture and self._sheep_can_be_moved_this_turn(pasture):
            self._choose_pasture(pasture)
        elif pasture and pasture.is_targeted and self.chosen_pasture is not None:
            self._choose_target_pasture(pasture)
        else:
            self._remove_marked_pastures()

    def scroll_up(self) -> None:
        self._add_sheep_to_planned_move()

    def scroll_down(self) -> None:
        self._subtract_sheep_from_planned_move()

    def press_enter(self) -> None:
        if self._are_pastures_chosen():
            self._move_sheep()
            self.next_turn()
            self.latest_value = self.evaluate_game_state()

    # Vuorot

    def get_number_of_turn(self) -> int:
        return self._turn

    def is_in_initial_placement(self) -> bool:
        return self._turn <= 2

    def is_computers_turn(self) -> bool:
        return not self.is_players_turn

    def is_input_allowed(self) -> bool:
        if self._is_simulation:
            return False
        if not self.is_players_turn:
            return False
        return not self.is_over_for_player()

    def is_next_move_calculated(self) -> bool:
        if self.is_players_turn:
            if self._is_simulation:
                return not self.is_over_for_player()
            return False
        return not self.is_over_for_computer()

    def next_turn(self) -> None:
        if self.is_over_for_computer():
            self.is_players_turn = True
        elif self.is_over_for_player():
            self.is_players_turn = False
        else:
            self.is_players_turn = not self.is_players_turn

        self._turn += 1
        self._remove_marked_pastures()

    def _previous_turn(self) -> None:
        self._turn -= 1
        self._remove_marked_pastures()

        if self._winner is not None:
            self._winner = None

        if self.is_over_for_computer():
            self.is_players_turn = True
        elif self.is_over_for_player():
            self.is_players_turn = False
        else:
            self.is_players_turn = not self.is_players_turn

    def get_depth(self) -> int:
        if self._is_simulation and self.is_players_turn:
            return SIMULATED_PLAYER_DEPTH
        return DEPTH

    # Muuttujien nollaus

    def _remove_planned_sheep(self) -> None:
        for pasture in self.pastures:
            pasture.planned_sheep = None

    def _remove_marked_pastures(self) -> None:
        self.chosen_pasture = None
        self.target_pasture = None

        for pasture in self.pastures:
            pasture.is_targeted = False
            pasture.planned_sheep = None

    # Heuristiikka

    def _calculate_player_won(self) -> bool:
        return self.is_over_for_computer() and self.calculate_winner() == PLAYER

    def _calculate_computer_won(self) -> bool:
        return self.is_over_for_player() and self.calculate_winner() == COMPUTER

    def evaluate_game_state(self) -> float:
        if self._calculate_player_won():
            return float('inf')
        if self._calculate_computer_won():
            return float('-inf')

        return sum(pasture.get_value(self.pastures) for pasture in self.get_potential_sheep_to_move())

    # Pelin päättyminen

    def _are_no_potential_moves(self, pastures: List[Pasture]) -> bool:
        for pasture in pastures:
            if pasture.are_any_potential_targets(self.pastures):
                return False
        return True

    def is_over_for_player(self) -> bool:
        if self.is_in_initial_placement():
            return False
        if self._winner is not None:
            return True
        pastures = self.get_pastures_occupied_by_player()
        return self._are_no_potential_moves(pastures)

    def is_over_for_computer(self) -> bool:
        if self.is_in_initial_placement():
            return False
        if self._winner is not None:
            return True
        pastures = self.get_pastures_occupied_by_computer()
        return self._are_no_potential_moves(pastures)

    def is_over_for_player_in_turn(self) -> bool:
        if self.is_in_initial_placement():
            return False
        if self._winner is not None:
            return True
        if self.is_players_turn:
            return self.is_over_for_player()
        return self.is_over_for_computer()

    def is_over(self) -> bool:
        if self.is_in_initial_placement():
            return False
        if self._winner is not None:
            return True
        pastures = self.get_occupied_pastures()
        is_over = self._are_no_potential_moves(pastures)
        if is_over:
            self._winner = self.calculate_winner()
        return is_over

    def _go_through_neighbours(self, pasture: Pasture, all_pastures: List[Pasture], herd_size: int) -> int:
        largest_herd = herd_size
        # Käydään läpi laitumen naapurit
        for neighbour in pasture.get_neighbours(all_pastures):
            # Poistetaan laidun itse käsiteltynä
            all_pastures_without_self: List[Pasture] = [
                p for p in all_pastures if p is not pasture]
            # Pidetään kirjaa suurimmasta löytyneestä alueesta
            largest_herd = max(largest_herd, self._go_through_neighbours(
                neighbour, all_pastures_without_self, herd_size + 1))

        return largest_herd

    def _find_largest_herd(self, pastures: List[Pasture]) -> int:
        """Etsii annettujen laidunten suurimman yhtenäisen alueen"""
        largest_herd = 0
        for pasture in pastures:
            largest_herd = max(largest_herd,
                               self._go_through_neighbours(pasture, pastures, 1))
        return largest_herd

    def get_players_largest_herd(self) -> int:
        return self._find_largest_herd(self.get_pastures_occupied_by_player())

    def get_computers_largest_herd(self) -> int:
        return self._find_largest_herd(self.get_pastures_occupied_by_computer())

    def calculate_who_has_largest_herd(self) -> int | None:
        """Palauttaa pelaajan, jolla on suurin yhtenäinen laidunalue"""
        player_largest_herd = self.get_players_largest_herd()
        computers_largest_herd = self.get_computers_largest_herd()
        if player_largest_herd > computers_largest_herd:
            return PLAYER
        if computers_largest_herd > player_largest_herd:
            return COMPUTER
        return None

    def calculate_winner(self) -> int | None:
        if self._winner is not None:
            return self._winner

        players_pastures = self.get_amount_of_pastures_occupied_by_player()
        computers_pastures = self.get_amount_of_pastures_occupied_by_computer()

        if players_pastures > computers_pastures:
            return PLAYER
        if computers_pastures > players_pastures:
            return COMPUTER
        return self.calculate_who_has_largest_herd()

    # Laitumet

    def is_occupied_by_player_in_turn(self, pasture: Pasture) -> bool:
        """Palauttaa tosi, mikäli laidun on vuorossa olevan pelaajan miehittämä"""
        if pasture.is_free():
            return False
        return self.is_players_turn == pasture.is_occupied_by_player()

    def _are_pastures_chosen(self) -> bool:
        return self.chosen_pasture is not None and self.target_pasture is not None

    def get_occupied_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_occupied(), self.pastures))

    def get_pastures_occupied_by_player(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_occupied_by_player(), self.pastures))

    def get_amount_of_pastures_occupied_by_player(self) -> int:
        return len(self.get_pastures_occupied_by_player())

    def get_pastures_occupied_by_computer(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_occupied_by_computer(), self.pastures))

    def get_amount_of_pastures_occupied_by_computer(self) -> int:
        return len(self.get_pastures_occupied_by_computer())

    def get_amount_of_targeted_pastures(self) -> int:
        return sum(1 for pasture in self.pastures if pasture.is_targeted)

    def get_amount_of_edge_pastures(self) -> int:
        return sum(1 for pasture in self.pastures if pasture.is_on_edge(self.pastures))

    def is_equal_amount_of_pastures_occupied(self) -> bool:
        return self.get_amount_of_pastures_occupied_by_player() == self.get_amount_of_pastures_occupied_by_computer()

    def is_focused(self, pasture: Pasture, pointed_at: bool) -> bool:
        if self._is_simulation:
            return False
        if self._winner is not None:
            return False
        if (pasture is self.chosen_pasture or
            pasture.is_targeted or
                pasture.get_amount_of_planned_sheep() > 0):
            return True
        if pointed_at:
            return (self.is_in_initial_placement() and
                    pasture.is_potential_initial_pasture(self.pastures)) or (
                self.is_players_turn and pasture.is_occupied_by_player())
        return False

    # Siirrot

    def _choose_pasture(self, pasture):
        if self.target_pasture is not None:
            self.target_pasture = None
            self._remove_planned_sheep()

        self.chosen_pasture = pasture
        targets = pasture.get_potential_targets(self.pastures)
        for p in self.pastures:
            p.is_targeted = p in targets

    def _choose_target_pasture(self, pasture):
        if self.target_pasture is not None:
            self._remove_planned_sheep()

        self.target_pasture = pasture
        self.target_pasture.planned_sheep = 1
        self.chosen_pasture.planned_sheep = self.chosen_pasture.get_amount_of_sheep() - 1

    def get_potential_initial_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_potential_initial_pasture(self.pastures), self.pastures))

    def get_potential_sheep_to_move(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_possible_to_move(self.pastures), self.pastures))

    def _sheep_can_be_moved_this_turn(self, pasture: Pasture) -> bool:
        return pasture.is_possible_to_move(self.pastures) and self.is_occupied_by_player_in_turn(pasture)

    def get_potential_sheep_to_move_this_turn(self) -> List[Pasture]:
        return list(filter(self._sheep_can_be_moved_this_turn, self.pastures))

    def _move_sheep(self) -> None:
        """Siirtää suunnitellut lampaat kohdelaitumelle."""
        if self.chosen_pasture is None or self.target_pasture is None or self.chosen_pasture.occupier is None:
            raise SystemError('Pastures are missing')
        self.chosen_pasture.occupy(
            self.chosen_pasture.occupier, self.chosen_pasture.get_amount_of_planned_sheep())
        self.target_pasture.occupy(
            self.chosen_pasture.occupier, self.target_pasture.get_amount_of_planned_sheep())
        self.chosen_pasture.planned_sheep = None
        self.target_pasture.planned_sheep = None

    # Lampaiden asetus

    def _place_initial_sheep(self, pasture: Pasture) -> None:
        """Asettaa aloituslampaat annetulle laitumelle"""
        pasture.occupy(
            PLAYER if self.is_players_turn else COMPUTER, self.initial_sheep)

    def _add_sheep_to_planned_move(self):
        if self._are_pastures_chosen() and self.chosen_pasture.get_amount_of_planned_sheep() >= 2:
            self.chosen_pasture.subtract_a_planned_sheep()
            self.target_pasture.add_a_planned_sheep()

    def _subtract_sheep_from_planned_move(self):
        if self._are_pastures_chosen() and self.target_pasture.get_amount_of_planned_sheep() >= 2:
            self.chosen_pasture.add_a_planned_sheep()
            self.target_pasture.subtract_a_planned_sheep()

    def make_initial_turn(self, pasture: Pasture) -> None:
        self._place_initial_sheep(pasture)
        self.next_turn()

    def undo_initial_turn(self, pasture: Pasture) -> None:
        pasture.reset()
        self._previous_turn()

    def make_normal_turn(self, pasture: Pasture, target: Pasture, sheep: int) -> None:
        pasture.planned_sheep = pasture.get_amount_of_sheep() - sheep
        target.planned_sheep = target.get_amount_of_sheep() + sheep

        self.chosen_pasture = pasture
        self.target_pasture = target

        self._move_sheep()
        self.next_turn()

    def undo_normal_turn(self, pasture: Pasture, target_pasture: Pasture, sheep: int) -> None:
        if pasture.occupier is None:
            raise ValueError('Pasture occupier not found')
        pasture.occupy(
            pasture.occupier, pasture.get_amount_of_sheep() + sheep)
        target_pasture.reset()
        self._previous_turn()
