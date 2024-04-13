from typing import List, Tuple
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

    def evaluate_game_state(self) -> float:
        value: float = 0
        for pasture in self.pastures:
            if pasture.is_taken():
                free_neighbours = pasture.get_amount_of_free_neighbours(
                    self.pastures)
                free_neighbours_value = free_neighbours * pasture.get_amount_of_sheep()
                friendly_neighbours = pasture.get_amount_of_free_neighbours(
                    self.pastures)
                if pasture.is_owned_by_human():
                    # Ihmiselle yksi piste jokaisesta tyhjästä naapurilaitumesta kerrottuna lampaiden määrällä
                    value += free_neighbours_value
                    # Ihmiselle kymmenesosapiste jokaisesta omasta naapurilaitumesta
                    value += friendly_neighbours * 0.1
                else:
                    value -= free_neighbours_value
                    value -= friendly_neighbours * 0.01
        print('Pelitilanteen arvo on ' + str(value))
        return value

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

        # Tarkastetaan, onko peli ohi
        self.is_over()
        if self.is_humans_turn and not self.is_over_for_ai:
            # Pelaajan vuoro siirtyy tekoälylle, koska tekoäly ei ole hävinnyt
            self.is_humans_turn = False
        elif not self.is_humans_turn and not self.is_over_for_human:
            # Tekoälyn vuoro siirtyy pelaajalle, koska pelaaja ei ole hävinnyt
            self.is_humans_turn = True

        self.turn += 1

    def previous_turn(self):
        self.is_humans_turn = not self.is_humans_turn
        self.turn -= 1

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
        if self.are_pastures_chosen() and self.chosen_pasture.planned_sheep >= 2:
            self.chosen_pasture.deduct_a_sheep()
            self.target_pasture.add_a_sheep()

    def try_to_subtract_sheep_from_planned_move(self):
        if self.are_pastures_chosen() and self.target_pasture.planned_sheep >= 2:
            self.chosen_pasture.add_a_sheep()
            self.target_pasture.deduct_a_sheep()

    def add_sheep_to_target(self, times: int):
        for _ in range(times):
            self.try_to_add_sheep_to_planned_move()

    def subtract_sheep_from_target(self, times: int):
        for _ in range(times):
            self.try_to_subtract_sheep_from_planned_move()

    def sheep_can_be_moved(self, pasture: Pasture) -> bool:
        return self.is_controlled_by_player_in_turn(pasture) and pasture.sheep is not None and pasture.sheep > 1 and not pasture.is_surrounded(self.pastures)

    def get_potential_sheep_to_move(self) -> List[Pasture]:
        return list(filter(
            self.sheep_can_be_moved, self.pastures))

    def get_potential_initial_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_free() and pasture.is_on_edge(self.pastures), self.pastures))

    def get_pasture_from_position(self, position: Tuple[float, float]) -> Pasture | None:
        for pasture in self.pastures:
            if pasture.position == position:
                return pasture
        return None

    def make_ai_move(self, pasture: Pasture | None, target: Pasture | None, sheep: int | None):
        if pasture is not None:
            if target is None and sheep == INITIAL_SHEEP:
                initial_pasture = self.get_pasture_from_position(
                    pasture.position)
                if not initial_pasture:
                    raise ValueError(
                        "Pastures were not found.")
                self.make_initial_turn(initial_pasture)
            elif target is not None and sheep is not None:
                from_pasture = self.get_pasture_from_position(
                    pasture.position)
                to_pasture = self.get_pasture_from_position(
                    target.position)
                if not from_pasture or not to_pasture:
                    raise ValueError(
                        "Pastures were not found.")
                self.make_normal_turn(from_pasture, to_pasture, sheep)

    def human_has_larger_continuous_pasture(self):
        # Toteutus vaatii vielä parantelua
        human_friendly_neighbours = 0
        ai_friendly_neighbours = 0
        for pasture in self.pastures:
            friendly_neighbours = len(
                pasture.get_friendly_neighbours(self.pastures))
            if pasture.is_owned_by_human():
                human_friendly_neighbours += friendly_neighbours
            else:
                ai_friendly_neighbours += friendly_neighbours
        return human_friendly_neighbours > ai_friendly_neighbours

    def calculate_human_won(self) -> bool | None:
        if not self.is_over():
            return None
        human_points = 0
        ai_points = 0
        for pasture in self.pastures:
            if pasture.is_taken():
                if pasture.is_owned_by_human():
                    human_points += 1
                else:
                    ai_points += 1
        if human_points == ai_points:
            return self.human_has_larger_continuous_pasture()
        return human_points > ai_points

    def get_winner_text(self) -> str:
        human_won = self.calculate_human_won()
        if human_won is None:
            return 'Virhe'
        return 'Pelaaja voitti!' if human_won else 'Tietokone voitti!'

    def remove_planned_sheep(self):
        for pasture in self.pastures:
            pasture.planned_sheep = None

    def click_on_pasture(self, pasture: Pasture):
        if self.is_in_initial_placement():
            if pasture.is_on_edge(self.pastures) and not pasture.is_taken():
                self.make_initial_turn(pasture)
        else:  # Aloituslampaat on jo asetettu
            if pasture.is_taken() and self.is_controlled_by_player_in_turn(pasture):
                # Valitaan lähtöruutu
                self.chosen_pasture = pasture
                if self.target_pasture is not None:
                    self.remove_planned_sheep()
                    self.target_pasture = None
                targets = pasture.get_potential_targets(
                    self.pastures)
                for pasture in self.pastures:
                    if pasture in targets:
                        pasture.targeted = True
                    else:
                        pasture.targeted = False
            elif pasture.targeted and self.chosen_pasture is not None and self.chosen_pasture.sheep is not None and pasture is not self.chosen_pasture:
                # Jos lähtöruutu valittu, valitaan kohderuutu
                if self.target_pasture is not None:
                    self.remove_planned_sheep()
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

    def should_be_focused(self, pasture: Pasture, pointed_at: bool) -> bool:
        if pasture is self.chosen_pasture:
            return True
        elif pasture.targeted:
            return True
        elif pasture.planned_sheep is not None:
            return True
        elif pointed_at:
            if self.is_in_initial_placement() and pasture.is_on_edge(self.pastures) and pasture.is_free():
                return True
            elif not self.is_in_initial_placement() and pasture.is_taken() and self.is_controlled_by_player_in_turn(pasture):
                return True
        return False

    def make_initial_turn(self, pasture):
        self.place_initial_sheep(pasture)
        self.next_turn()

    def undo_initial_move(self, pasture: Pasture) -> None:
        pasture.reset()
        self.previous_turn()

    def make_normal_turn(self, pasture: Pasture, target_pasture: Pasture, amount_of_sheep: int) -> None:
        self.click_on_pasture(pasture)
        self.click_on_pasture(target_pasture)
        self.add_sheep_to_target(amount_of_sheep)
        self.confirm_move()

    def undo_move(self, pasture: Pasture, target_pasture: Pasture, sheep: int) -> None:
        pasture.add_permanent_sheep(sheep)
        target_pasture.reset()
        self.previous_turn()
