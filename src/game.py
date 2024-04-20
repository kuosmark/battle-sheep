from typing import List, Tuple
from move import Move
from pasture import Pasture

INITIAL_SHEEP = 16


class Game:
    def __init__(self) -> None:
        self.pastures = self.init_pastures()
        self.turn = 1
        self.is_humans_turn = True
        self.chosen_pasture: Pasture | None = None
        self.target_pasture: Pasture | None = None

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

    # Vuorot

    def is_in_initial_placement(self) -> bool:
        return self.turn <= 2

    def next_turn(self) -> None:
        self.remove_marked_pastures()
        if self.is_humans_turn and not self.is_over_for_ai():
            # Pelaajan vuoro siirtyy tekoälylle, joka ei ole vielä hävinnyt
            self.is_humans_turn = False
            self.turn += 1
        elif not self.is_humans_turn and not self.is_over_for_player():
            # Tekoälyn vuoro siirtyy pelaajalle, joka ei ole vielä hävinnyt
            self.is_humans_turn = True
            self.turn += 1
        elif not self.is_over():
            # Peli ei ole vielä ohi, joten sama pelaaja jatkaa
            self.turn += 1

    # Tämä ei toimi jos toinen pelaaja on jo hävinnyt
    def previous_turn(self) -> None:
        self.is_humans_turn = not self.is_humans_turn
        self.turn -= 1

    # Muuttujien nollaus

    def remove_planned_sheep(self) -> None:
        for pasture in self.pastures:
            pasture.planned_sheep = None

    def remove_targets_and_planned_sheep(self) -> None:
        for pasture in self.pastures:
            pasture.targeted = False
            pasture.planned_sheep = None

    def remove_marked_pastures(self) -> None:
        self.chosen_pasture = None
        self.target_pasture = None
        self.remove_targets_and_planned_sheep()

    # Onko peli ohi?

    def are_no_potential_moves(self, pastures: List[Pasture]) -> bool:
        for pasture in pastures:
            potential_moves = pasture.get_potential_targets(self.pastures)
            if len(potential_moves) > 0:
                return False
        return True

    def is_over_for_player(self) -> bool:
        if self.is_in_initial_placement():
            return False
        players_pastures = list(filter(
            lambda pasture: pasture.is_occupied_by_player(), self.get_occupied_pastures()))
        return self.are_no_potential_moves(players_pastures)

    def is_over_for_ai(self) -> bool:
        if self.is_in_initial_placement():
            return False
        ais_pastures = list(filter(
            lambda pasture: not pasture.is_occupied_by_player(), self.get_occupied_pastures()))
        return self.are_no_potential_moves(ais_pastures)

    def is_over(self) -> bool:
        if self.is_in_initial_placement():
            return False
        return self.are_no_potential_moves(self.get_occupied_pastures())

    # Laitumet

    def get_pasture_in_position(self, position: Tuple[float, float]) -> Pasture | None:
        for pasture in self.pastures:
            if pasture.collide_with_point(position):
                return pasture
        return None

    def get_pasture_in_exact_position(self, position: Tuple[float, float]) -> Pasture | None:
        for pasture in self.pastures:
            if pasture.position == position:
                return pasture
        return None

    def is_controlled_by_player_in_turn(self, pasture: Pasture) -> bool:
        return self.is_humans_turn == pasture.is_occupied_by_player()

    def are_pastures_chosen(self) -> bool:
        return self.chosen_pasture is not None and self.target_pasture is not None

    def get_occupied_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_occupied(), self.pastures))

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
            elif not self.is_in_initial_placement() and pasture.is_occupied() and self.is_controlled_by_player_in_turn(pasture):
                return True
        return False

    # Mahdolliset siirrot

    def sheep_can_be_moved(self, pasture: Pasture) -> bool:
        return self.is_controlled_by_player_in_turn(pasture) and pasture.get_amount_of_sheep() > 1 and not pasture.is_surrounded(self.pastures)

    def get_potential_initial_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_free() and pasture.is_on_edge(self.pastures), self.pastures))

    def get_potential_sheep_to_move(self) -> List[Pasture]:
        return list(filter(
            self.sheep_can_be_moved, self.pastures))

    # Lampaiden asetus

    def place_initial_sheep(self, pasture: Pasture) -> None:
        """Asettaa aloituslampaat annetulle laitumelle"""
        player = 0 if self.is_humans_turn else 1
        if pasture.is_free() and pasture.is_on_edge(self.pastures):
            pasture.update_sheep(player, INITIAL_SHEEP)
        else:
            raise ValueError(
                "The given pasture is not suitable for placing sheep.")

    def try_to_add_sheep_to_planned_move(self, amount: int):
        if self.chosen_pasture is None or self.target_pasture is None:
            raise SystemError('Pasture and/or target not set')

        chosen_planned_sheep = self.chosen_pasture.get_amount_of_planned_sheep()
        target_planned_sheep = self.target_pasture.get_amount_of_planned_sheep()
        if chosen_planned_sheep - amount >= 1 or target_planned_sheep + amount < INITIAL_SHEEP:
            self.chosen_pasture.subtract_planned_sheep(amount)
            self.target_pasture.add_planned_sheep(amount)

    def try_to_subtract_sheep_from_planned_move(self, amount: int):
        if self.chosen_pasture is None or self.target_pasture is None:
            raise SystemError('Pasture and/or target not set')

        chosen_planned_sheep = self.chosen_pasture.get_amount_of_planned_sheep()
        target_planned_sheep = self.target_pasture.get_amount_of_planned_sheep()
        if chosen_planned_sheep + amount < INITIAL_SHEEP and target_planned_sheep - amount >= 1:
            self.target_pasture.subtract_planned_sheep(amount)
            self.chosen_pasture.add_planned_sheep(amount)

    def click(self, position: Tuple[float, float]) -> None:
        clicked_pasture = self.get_pasture_in_position(position)
        if clicked_pasture:
            self.click_on_pasture(clicked_pasture)
        else:
            self.remove_marked_pastures()

    def click_on_pasture(self, pasture: Pasture) -> None:
        if self.is_in_initial_placement():
            if pasture.is_on_edge(self.pastures) and not pasture.is_occupied():
                self.make_initial_turn(pasture)
        else:  # Aloituslampaat on jo asetettu
            if pasture.is_occupied() and self.is_controlled_by_player_in_turn(pasture):
                # Valitaan lähtöruutu
                self.chosen_pasture = pasture
                if self.target_pasture is not None:
                    self.remove_planned_sheep()
                    self.target_pasture = None
                targets = pasture.get_potential_targets(
                    self.pastures)
                for p in self.pastures:
                    if p in targets:
                        p.targeted = True
                    else:
                        p.targeted = False
            elif pasture.targeted and self.chosen_pasture is not None and self.chosen_pasture.sheep is not None and pasture is not self.chosen_pasture:
                # Jos lähtöruutu valittu, valitaan kohderuutu
                if self.target_pasture is not None:
                    self.remove_planned_sheep()
                self.target_pasture = pasture
                pasture.planned_sheep = 1
                self.chosen_pasture.planned_sheep = self.chosen_pasture.sheep - 1
            else:
                self.remove_marked_pastures()

    def confirm_move(self):
        if self.target_pasture is not None and self.target_pasture.planned_sheep > 0 and self.chosen_pasture is not None and self.chosen_pasture.planned_sheep > 0:
            self.chosen_pasture.move_sheep_to(self.target_pasture)
            self.next_turn()

    # Tekoälyn siirto

    def make_ai_move(self, move: Move):
        if move.pasture is not None:
            if move.is_initial():
                initial_pasture = self.get_pasture_in_exact_position(
                    move.pasture.position)
                if not initial_pasture:
                    raise ValueError(
                        "Pastures were not found.")
                self.make_initial_turn(initial_pasture)
            elif move.target is not None and move.sheep is not None:
                from_pasture = self.get_pasture_in_exact_position(
                    move.pasture.position)
                to_pasture = self.get_pasture_in_exact_position(
                    move.target.position)
                if not from_pasture or not to_pasture:
                    raise ValueError(
                        "Pastures were not found.")
                self.make_normal_turn(from_pasture, to_pasture, move.sheep)

    def make_initial_turn(self, pasture: Pasture) -> None:
        self.place_initial_sheep(pasture)
        self.next_turn()

    def undo_initial_move(self, pasture: Pasture) -> None:
        pasture.reset()
        self.previous_turn()

    def make_normal_turn(self, pasture: Pasture, target_pasture: Pasture, amount_of_sheep: int) -> None:
        self.click_on_pasture(pasture)
        self.click_on_pasture(target_pasture)
        self.try_to_add_sheep_to_planned_move(amount_of_sheep)
        self.confirm_move()

    def undo_move(self, pasture: Pasture, target_pasture: Pasture, sheep: int) -> None:
        if pasture.occupier is None:
            raise ValueError('Pasture occupier not found')
        pasture.update_sheep(pasture.occupier, sheep)
        target_pasture.reset()
        self.previous_turn()

    # Heuristiikka ja voittajan laskenta

    def evaluate_game_state(self) -> float:
        # Palautetaan paras tai huonoin mahdollinen arvo voittajan mukaan, mikäli peli on ohi
        if self.is_over():
            if self.calculate_human_won():
                return float('Inf')
            return float('-Inf')

        value: float = 0
        for pasture in self.pastures:
            if pasture.is_occupied():
                sheep = pasture.get_amount_of_sheep()
                is_pasture_surrounded = pasture.is_surrounded(self.pastures)
                free_neighbours = pasture.get_amount_of_free_neighbours(
                    self.pastures)
                free_neighbours_value = free_neighbours * sheep
                friendly_neighbours = pasture.get_amount_of_friendly_neighbours(
                    self.pastures)
                if pasture.is_occupied_by_player():
                    # Jokaisesta tyhjästä naapurilaitumesta piste kerrottuna lampaiden määrällä
                    value += free_neighbours_value
                    # Kymmenesosapiste jokaisesta omasta naapurilaitumesta
                    value += friendly_neighbours * 0.1
                    if is_pasture_surrounded:
                        # Jokaisesta ansaan jääneestä lampaasta miinuspiste
                        value -= sheep
                else:
                    value -= free_neighbours_value
                    value -= friendly_neighbours * 0.01
                    if is_pasture_surrounded:
                        value += sheep
        print('Pelitilanteen arvo on ' + str(value))
        return value

    def human_has_larger_continuous_pasture(self) -> bool:
        # Toteutus vaatii vielä parantelua
        human_friendly_neighbours = 0
        ai_friendly_neighbours = 0
        for pasture in self.pastures:
            friendly_neighbours = len(
                pasture.get_friendly_neighbours(self.pastures))
            if pasture.is_occupied_by_player():
                human_friendly_neighbours += friendly_neighbours
            else:
                ai_friendly_neighbours += friendly_neighbours
        return human_friendly_neighbours > ai_friendly_neighbours

    def calculate_human_won(self) -> bool:
        human_points = 0
        ai_points = 0
        for pasture in self.pastures:
            if pasture.is_occupied():
                if pasture.is_occupied_by_player():
                    human_points += 1
                else:
                    ai_points += 1
        if human_points == ai_points:
            return self.human_has_larger_continuous_pasture()
        return human_points > ai_points

    def get_winner_text(self) -> str:
        if not self.is_over():
            return 'Virhe'
        return 'Pelaaja voitti!' if self.calculate_human_won() else 'Tietokone voitti!'
