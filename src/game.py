from typing import List

from pasture import Pasture

INITIAL_SHEEP = 16


class Game:
    def __init__(self, pastures: List[Pasture]) -> None:
        self.pastures = pastures
        self.turn = 1
        self.is_humans_turn = True
        self.chosen_pasture: Pasture | None = None
        self.target_pasture: Pasture | None = None

    def is_in_initial_placement(self) -> bool:
        return self.turn <= 2

    def remove_targets(self):
        for pasture in self.pastures:
            pasture.targeted = False

    def next_turn(self) -> None:
        if not self.is_in_initial_placement():
            self.chosen_pasture = None
            self.target_pasture = None
            self.remove_targets()
        self.turn += 1
        self.is_humans_turn = not self.is_humans_turn

    def is_over(self) -> bool:
        # Peli ei voi olla ohi, mikäli lampaita ei ole vielä asetettu
        if self.is_in_initial_placement():
            return False
        # Tarkistetaan, voiko pelaaja tehdä siirtoa
        for pasture in self.pastures:
            if pasture.is_taken() and pasture.is_owned_by_human() == self.is_humans_turn:
                potential_moves = pasture.get_potential_targets(self.pastures)
                # Peli ei ole ohi, mikäli mahdollinen siirto löytyy
                if len(potential_moves) > 0:
                    return False
        return True

    def place_initial_sheep(self, pasture: Pasture) -> None:
        """Asettaa aloituslampaat annetulle laitumelle"""
        player = 0 if self.is_humans_turn else 1
        pasture.update_sheep(player, INITIAL_SHEEP)

    def is_controlled_by_player_in_turn(self, pasture: Pasture) -> bool:
        return self.is_humans_turn == pasture.is_owned_by_human()

    def try_to_add_sheep_to_planned_move(self):
        if self.chosen_pasture.planned_sheep >= 2:
            self.chosen_pasture.deduct_a_sheep()
            self.target_pasture.add_a_sheep()

    def try_to_subtract_sheep_from_planned_move(self):
        if self.target_pasture.planned_sheep >= 2:
            self.chosen_pasture.add_a_sheep()
            self.target_pasture.deduct_a_sheep()
