from typing import List
from constants import (
    COMPUTER,
    PLAYER,
)
from pasture import Pasture
from utils import calculate_initial_sheep, init_pastures


class Game:
    def __init__(self, board_height: int, board_width: int, is_simulation: bool) -> None:
        self.pastures: List[Pasture] = init_pastures(board_height, board_width)
        self.initial_sheep: int = calculate_initial_sheep(
            board_height, board_width)
        self.is_simulation = is_simulation
        self._turn: int = 1
        self.is_players_turn = True
        self._winner: int | None = None
        self.chosen_pasture: Pasture | None = None
        self.target_pasture: Pasture | None = None

    # Syötteet

    def click_on_pasture(self, pasture: Pasture | None) -> None:
        """Käsittelee annetun laitumen painalluksen"""
        if (self.is_in_initial_placement()
            and pasture
                and pasture.is_potential_initial_pasture(self.pastures)):
            self.make_initial_turn(pasture)
        elif pasture and self._can_sheep_be_moved_this_turn(pasture):
            self._choose_pasture(pasture)
        elif pasture and pasture.is_targeted and self.chosen_pasture is not None:
            self._choose_target_pasture(pasture)
        else:
            self._remove_marked_pastures()

    def scroll_up(self) -> None:
        """Käsittelee hiiren rullan kelaamisen ylöspäin"""
        self._add_sheep_to_planned_move()

    def scroll_down(self) -> None:
        """Käsittelee hiiren rullan kelaamisen alaspäin"""
        self._subtract_sheep_from_planned_move()

    def press_enter(self) -> None:
        """Käsittelee Enter-painikkeen painalluksen"""
        if self._are_pastures_chosen():
            self._move_sheep()
            self.next_turn()

    # Vuorot

    def get_number_of_turn(self) -> int:
        """Palauttaa kuluvan vuoron järjestysluvun"""
        return self._turn

    def is_in_initial_placement(self) -> bool:
        """Palauttaa tosi, jos aloituslaitumia ei ole valittu"""
        return self._turn <= 2

    def is_input_allowed(self) -> bool:
        """Palauttaa tosi, jos pelaaja saa tehdä siirron"""
        if self.is_simulation:
            return False
        if not self.is_players_turn:
            return False
        return not self.is_over_for_player()

    def is_next_move_calculated(self) -> bool:
        """Palauttaa tosi, jos ohjelma laskee seuraava siirron"""
        if self.is_players_turn:
            if self.is_simulation:
                return not self.is_over_for_player()
            return False
        return not self.is_over_for_computer()

    def next_turn(self) -> None:
        """Siirtyy seuraavaan vuoroon"""
        if self.is_over_for_computer():
            self.is_players_turn = True
        elif self.is_over_for_player():
            self.is_players_turn = False
        else:
            self.is_players_turn = not self.is_players_turn

        self._turn += 1
        self._remove_marked_pastures()

    def _previous_turn(self) -> None:
        """Palaa edelliseen vuoroon"""
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

    # Muuttujien nollaus

    def _remove_planned_sheep(self) -> None:
        """Tyhjentää pelilaudan laitumien suunnitellut lampaat"""
        for pasture in self.pastures:
            pasture.planned_sheep = None

    def _remove_marked_pastures(self) -> None:
        """Tyhjentää suunnitellun vuoron"""
        self.chosen_pasture = None
        self.target_pasture = None

        for pasture in self.pastures:
            pasture.is_targeted = False
            pasture.planned_sheep = None

    # Heuristiikka

    def evaluate_game_state(self) -> float:
        """Palauttaa pelitilanteen heuristisen arvon"""
        if self.is_over_for_computer() and self.calculate_winner() == PLAYER:
            return float('inf')
        if self.is_over_for_player() and self.calculate_winner() == COMPUTER:
            return float('-inf')

        return sum(
            pasture.get_value(self.pastures) for pasture in self.get_potential_pastures_to_choose())

    # Pelin päättyminen

    def _are_no_potential_moves(self, pastures: List[Pasture]) -> bool:
        """Palauttaa tosi, jos annetuista laitumista ei voi tehdä siirtoja"""
        for pasture in pastures:
            if pasture.are_any_potential_targets(self.pastures):
                return False
        return True

    def is_over_for_player(self) -> bool:
        """Palauttaa tosi, jos pelaaja ei voi enää tehdä siirtoja"""
        if self.is_in_initial_placement():
            return False
        if self._winner is not None:
            return True
        pastures = self.get_pastures_occupied_by_player()
        return self._are_no_potential_moves(pastures)

    def is_over_for_computer(self) -> bool:
        """Palauttaa tosi, jos tekoäly ei voi enää tehdä siirtoja"""
        if self.is_in_initial_placement():
            return False
        if self._winner is not None:
            return True
        pastures = self.get_pastures_occupied_by_computer()
        return self._are_no_potential_moves(pastures)

    def is_over(self) -> bool:
        """Palauttaa tosi, jos peli on ohi"""
        if self.is_in_initial_placement():
            return False
        if self._winner is not None:
            return True
        pastures = self.get_occupied_pastures()
        is_over = self._are_no_potential_moves(pastures)
        if is_over:
            self._winner = self.calculate_winner()
        return is_over

    def _find_largest_herd(self, pasture: Pasture, pastures: List[Pasture], herd: int) -> int:
        """Palauttaa suurimman yhtenäisen alueen, johon annettu laidun kuuluu"""
        largest_herd = herd
        # Käydään läpi laitumen naapurit
        for neighbour in pasture.get_neighbours(pastures):
            # Poistetaan laidun itse käsiteltynä
            all_pastures_without_self: List[Pasture] = [
                p for p in pastures if p is not pasture]
            # Pidetään kirjaa suurimmasta löytyneestä alueesta
            largest_herd = max(largest_herd, self._find_largest_herd(
                neighbour, all_pastures_without_self, herd + 1))

        return largest_herd

    def get_players_largest_herd(self) -> int:
        """Palauttaa pelaajan laidunten suurimman yhtenäisen alueen koon"""
        largest_herd = 0
        pastures = self.get_pastures_occupied_by_player()
        for pasture in pastures:
            largest_herd = max(largest_herd,
                               self._find_largest_herd(pasture, pastures, 1))
        return largest_herd

    def get_computers_largest_herd(self) -> int:
        """Palauttaa tekoälyn laidunten suurimman yhtenäisen alueen koon"""
        largest_herd = 0
        pastures = self.get_pastures_occupied_by_computer()
        for pasture in pastures:
            largest_herd = max(largest_herd,
                               self._find_largest_herd(pasture, pastures, 1))
        return largest_herd

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
        """Palauttaa pelin voittajan olettaen, että peli on ohi"""
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
        """Palauttaa tosi, jos laidun on vuorossa olevan pelaajan miehittämä"""
        if pasture.is_free():
            return False
        return self.is_players_turn == pasture.is_occupied_by_player()

    def _are_pastures_chosen(self) -> bool:
        """Palauttaa tosi, jos sekä lähtö- että kohdelaidun on valittu"""
        return self.chosen_pasture is not None and self.target_pasture is not None

    def get_occupied_pastures(self) -> List[Pasture]:
        """Palauttaa miehitetyt laitumet"""
        return list(filter(lambda pasture: pasture.is_occupied(), self.pastures))

    def get_pastures_occupied_by_player(self) -> List[Pasture]:
        """Palauttaa pelaajan miehittämät laitumet"""
        return list(filter(lambda pasture: pasture.is_occupied_by_player(), self.pastures))

    def get_amount_of_pastures_occupied_by_player(self) -> int:
        """Palauttaa pelaajan miehittämien laidunten määrän"""
        return len(self.get_pastures_occupied_by_player())

    def get_pastures_occupied_by_computer(self) -> List[Pasture]:
        """Palauttaa tekoälyn miehittämät laitumet"""
        return list(filter(lambda pasture: pasture.is_occupied_by_computer(), self.pastures))

    def get_amount_of_pastures_occupied_by_computer(self) -> int:
        """Palauttaa tekoälyn miehittämien laidunten määrän"""
        return len(self.get_pastures_occupied_by_computer())

    def get_amount_of_targeted_pastures(self) -> int:
        """Palauttaa suunniteltujen kohdelaidunten määrän"""
        return sum(1 for pasture in self.pastures if pasture.is_targeted)

    def get_amount_of_edge_pastures(self) -> int:
        """Palauttaa pelilaudan reunalla olevien laidunten määrän"""
        return sum(1 for pasture in self.pastures if pasture.is_on_edge(self.pastures))

    def is_equal_amount_of_pastures_occupied(self) -> bool:
        """Palauttaa tosi, jos ottelijat miehittävät yhtä montaa laidunta"""
        return (self.get_amount_of_pastures_occupied_by_player()
                == self.get_amount_of_pastures_occupied_by_computer())

    def is_focused(self, pasture: Pasture, pointed_at: bool) -> bool:
        """Palauttaa tosi, jos annettu laidun kuuluisi valaista"""
        if self.is_simulation or self._winner is not None:
            return False
        if (pasture is self.chosen_pasture
            or pasture.is_targeted
                or pasture.get_amount_of_planned_sheep() > 0):
            return True
        if pointed_at:
            return ((self.is_in_initial_placement()
                     and pasture.is_potential_initial_pasture(self.pastures))
                    or (self.is_players_turn
                        and self._can_sheep_be_moved_this_turn(pasture)))
        return False

    # Siirrot

    def _choose_pasture(self, pasture):
        """Valitsee lähtölaitumen"""
        if self.target_pasture is not None:
            self.target_pasture = None
            self._remove_planned_sheep()

        self.chosen_pasture = pasture
        targets = pasture.get_potential_targets(self.pastures)
        for p in self.pastures:
            p.is_targeted = p in targets

    def _choose_target_pasture(self, pasture):
        """Valitsee kohdelaitumen"""
        if self.target_pasture is not None:
            self._remove_planned_sheep()

        self.target_pasture = pasture
        self.target_pasture.planned_sheep = 1
        self.chosen_pasture.planned_sheep = self.chosen_pasture.get_amount_of_sheep() - 1

    def get_potential_initial_pastures(self) -> List[Pasture]:
        """Palauttaa mahdolliset aloituslaitumet"""
        return list(filter(lambda p: p.is_potential_initial_pasture(self.pastures), self.pastures))

    def get_potential_pastures_to_choose(self) -> List[Pasture]:
        """Palauttaa mahdolliset lähtölaitumet"""
        return list(filter(lambda p: p.is_possible_to_move(self.pastures), self.pastures))

    def _can_sheep_be_moved_this_turn(self, pasture: Pasture) -> bool:
        """Palauttaa tosi, jos laitumelta voi siirtää lampaita kuluvalla vuorolla"""
        return (pasture.is_possible_to_move(self.pastures)
                and self.is_occupied_by_player_in_turn(pasture))

    def get_potential_pastures_to_choose_this_turn(self) -> List[Pasture]:
        """Palauttaa kuluvan vuoron mahdolliset lähtölaitumet"""
        return list(filter(self._can_sheep_be_moved_this_turn, self.pastures))

    def _move_sheep(self) -> None:
        """Siirtää suunnitellut lampaat lähtölaitumelta kohdelaitumelle"""
        if (self.chosen_pasture is None
            or self.target_pasture is None
                or self.chosen_pasture.occupier is None):
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
        """Lisää yhden lampaan suunniteltuun siirtoon"""
        if self._are_pastures_chosen() and self.chosen_pasture.get_amount_of_planned_sheep() >= 2:
            self.chosen_pasture.change_planned_sheep(-1)
            self.target_pasture.change_planned_sheep(1)

    def _subtract_sheep_from_planned_move(self):
        """Vähentää yhden lampaan suunnitellusta siirrosta"""
        if self._are_pastures_chosen() and self.target_pasture.get_amount_of_planned_sheep() >= 2:
            self.chosen_pasture.change_planned_sheep(1)
            self.target_pasture.change_planned_sheep(-1)

    def make_initial_turn(self, pasture: Pasture) -> None:
        """Tekee aloitussiirron, ja päättää vuoron"""
        self._place_initial_sheep(pasture)
        self.next_turn()

    def undo_initial_turn(self, pasture: Pasture) -> None:
        """Peruu aloitussiirron"""
        pasture.reset()
        self._previous_turn()

    def make_normal_turn(self, pasture: Pasture, target: Pasture, sheep: int) -> None:
        """Tekee tavallisen siirron, ja päättää vuoron"""
        pasture.planned_sheep = pasture.get_amount_of_sheep() - sheep
        target.planned_sheep = target.get_amount_of_sheep() + sheep

        self.chosen_pasture = pasture
        self.target_pasture = target

        self._move_sheep()
        self.next_turn()

    def undo_normal_turn(self, pasture: Pasture, target_pasture: Pasture, sheep: int) -> None:
        """Peruu tavallisen siirron"""
        if pasture.occupier is None:
            raise ValueError('Pasture occupier not found')
        pasture.occupy(
            pasture.occupier, pasture.get_amount_of_sheep() + sheep)
        target_pasture.reset()
        self._previous_turn()
