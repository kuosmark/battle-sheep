from typing import List
import random

from pasture import Pasture

INITIAL_SHEEP = 16


class Game:
    def __init__(self) -> None:
        self.pastures = self.init_pastures()
        self.turn = 1
        self.is_humans_turn = True
        self.chosen_pasture: Pasture | None = None
        self.target_pasture: Pasture | None = None
        self.is_over_for_ai = False
        self.is_over_for_human = False

    def init_pastures(self) -> List[Pasture]:
        """Luodaan heksagonilaitumista pelilauta"""
        x_length = 8
        y_length = 4
        initial_position = (50, 50)
        leftmost_pasture = Pasture(initial_position)
        pastures = [leftmost_pasture]

        for y_axis in range(y_length):
            if y_axis > 0:
                position = leftmost_pasture.vertices[2]
                leftmost_pasture = Pasture(position)
                pastures.append(leftmost_pasture)

            pasture = leftmost_pasture
            for x_axis in range(x_length - 1):
                (x, y) = pasture.position
                # Piirretään joka toinen laidun ylä- ja joka toinen alaviistoon edellisestä
                if x_axis % 2 == 1:
                    position = (x + pasture.radius * 3 / 2,
                                y - pasture.minimal_radius)
                else:
                    position = (x + pasture.radius * 3 / 2,
                                y + pasture.minimal_radius)
                pasture = Pasture(position)
                pastures.append(pasture)

        return pastures

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
        if pasture.is_free() and pasture.is_on_edge(self.pastures):
            pasture.update_sheep(player, INITIAL_SHEEP)
        else:
            raise ValueError(
                "The given pasture is not suitable for placing sheep.")

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

    def sheep_can_be_moved(self, pasture: Pasture) -> bool:
        return self.is_controlled_by_player_in_turn(pasture) and pasture.sheep is not None and pasture.sheep > 1 and not pasture.is_surrounded(self.pastures)

    def get_potential_sheep_to_move(self) -> List[Pasture]:
        return list(filter(
            self.sheep_can_be_moved, self.pastures))

    def get_potential_initial_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_free() and pasture.is_on_edge(self.pastures), self.pastures))

    def make_ai_move(self):
        if self.is_in_initial_placement():
            initial_pasture = random.choice(
                self.get_potential_initial_pastures())
            self.place_initial_sheep(initial_pasture)
        else:
            # Haetaan mahdolliset aloituslaitumet
            potential_pastures = self.get_potential_sheep_to_move()
            # Valitaan paras lähtölaidun
            chosen_pasture = random.choice(potential_pastures)
            potential_targets = chosen_pasture.get_potential_targets(
                self.pastures)
            # Valitaan paras kohdelaidun
            chosen_target = random.choice(potential_targets)
            # Valitaan paras lampaiden määrä
            chosen_target.planned_sheep = random.randrange(
                1, chosen_pasture.sheep)
            # Tehdään siirto
            chosen_pasture.planned_sheep = chosen_pasture.sheep - chosen_target.planned_sheep
            chosen_pasture.move_sheep_to(chosen_target)
        self.next_turn()

    def calculate_winner(self) -> str:
        human_points = 0
        ai_points = 0
        for pasture in self.pastures:
            if pasture.is_taken():
                if pasture.is_owned_by_human():
                    human_points += 1
                else:
                    ai_points += 1
        if human_points == ai_points:
            return 'Tasapeli!'
        elif human_points > ai_points:
            return 'Pelaaja voitti!'
        return 'Tietokone voitti!'

    def click_on_pasture(self, pasture: Pasture):
        if self.is_in_initial_placement():
            if pasture.is_on_edge(self.pastures) and not pasture.is_taken():
                self.place_initial_sheep(pasture)
                self.next_turn()
        else:  # Aloituslampaat on jo asetettu
            if pasture.is_taken() and self.is_controlled_by_player_in_turn(pasture):
                # Valitaan lähtöruutu
                self.chosen_pasture = pasture
                targets = pasture.get_potential_targets(
                    self.pastures)
                for target in targets:
                    target.targeted = True
            elif pasture.targeted and self.chosen_pasture is not None and self.chosen_pasture.sheep is not None and pasture is not self.chosen_pasture:
                # Jos lähtöruutu valittu, valitaan kohderuutu
                self.target_pasture = pasture
                pasture.planned_sheep = 1
                self.chosen_pasture.planned_sheep = self.chosen_pasture.sheep - 1

    def confirm_move(self):
        if self.target_pasture is not None and self.target_pasture.planned_sheep > 0 and self.chosen_pasture is not None and self.chosen_pasture.planned_sheep > 0:
            self.chosen_pasture.move_sheep_to(self.target_pasture)
            self.next_turn()

    def are_pastures_chosen(self) -> bool:
        return self.target_pasture is not None and self.chosen_pasture is not None

    def get_targeted_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.targeted is True, self.pastures))
