from typing import List
import random

from pasture import Pasture

INITIAL_SHEEP = 16


class Game:
    def __init__(self, pastures: List[Pasture]) -> None:
        self.pastures = pastures
        self.turn = 1
        self.is_humans_turn = True
        self.chosen_pasture: Pasture | None = None
        self.target_pasture: Pasture | None = None
        self.is_over_for_ai = False
        self.is_over_for_human = False

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

        if self.is_humans_turn and not self.is_over_for_ai:
            # Pelaajan vuoro siirtyy tekoälylle, koska tekoäly ei ole hävinnyt
            self.is_humans_turn = False
        elif not self.is_humans_turn and not self.is_over_for_human:
            # Tekoälyn vuoro siirtyy pelaajalle, koska pelaaja ei ole hävinnyt
            self.is_humans_turn = True

        self.turn += 1

    def is_over_for(self, human: bool) -> bool:
        for pasture in self.pastures:
            if pasture.is_taken() and pasture.is_owned_by_human() == human:
                potential_moves = pasture.get_potential_targets(self.pastures)
                # Peli ei ole ohi, mikäli mahdollinen siirto löytyy
                if len(potential_moves) > 0:
                    return False
        return True

    def is_over(self) -> bool:
        # Peli ei voi olla ohi, mikäli lampaita ei ole vielä asetettu
        if self.is_in_initial_placement():
            return False
        # Tarkistetaan, voiko pelaaja tehdä siirtoa
        human_game_over = self.is_over_for(True)
        if human_game_over:
            self.is_over_for_human = True
        ai_game_over = self.is_over_for(False)
        if ai_game_over:
            self.is_over_for_ai = True
        return human_game_over is True and ai_game_over is True

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

    def get_pastures_on_edge(self):
        return list(filter(lambda pasture: pasture.is_on_edge(
            self.pastures), self.pastures))

    def sheep_can_be_moved(self, pasture: Pasture) -> bool:
        return self.is_controlled_by_player_in_turn(pasture) and pasture.sheep is not None and pasture.sheep > 1 and not pasture.is_surrounded(self.pastures)

    def get_potential_sheep_to_move(self) -> List[Pasture]:
        return list(filter(
            self.sheep_can_be_moved, self.pastures))

    def make_random_ai_move(self):
        if self.is_in_initial_placement():
            edge_pastures = self.get_pastures_on_edge()
            initial_pasture = random.choice(edge_pastures)
            self.place_initial_sheep(initial_pasture)
        else:
            potential_pastures = self.get_potential_sheep_to_move()
            chosen_pasture = random.choice(potential_pastures)
            potential_targets = chosen_pasture.get_potential_targets(
                self.pastures)
            chosen_target = random.choice(potential_targets)
            chosen_target.planned_sheep = random.randrange(
                1, chosen_pasture.sheep)
            chosen_pasture.planned_sheep = chosen_pasture.sheep - chosen_target.planned_sheep
            chosen_pasture.move_sheep_to(chosen_target)
