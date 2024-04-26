from typing import List, Tuple
from constants import INITIAL_SHEEP, MINIMAL_RADIUS, PASTURE_RADIUS
from pasture import Pasture


class Game:
    def __init__(self) -> None:
        self.pastures = self._init_pastures()
        self._turn = 1
        self._is_humans_turn = True
        self.chosen_pasture: Pasture | None = None
        self.target_pasture: Pasture | None = None

    def __str__(self):
        return f'Peli, jossa vuoro on {self._turn} ja {'pelaajan' if self._is_humans_turn else 'tekoälyn'} siirto. Arvoltaan {self.evaluate_game_state()}'

    def _init_pastures(self) -> List[Pasture]:
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
                    position = (x + PASTURE_RADIUS * 3 / 2,
                                y - MINIMAL_RADIUS)
                else:
                    position = (x + PASTURE_RADIUS * 3 / 2,
                                y + MINIMAL_RADIUS)
                pasture = Pasture(position)
                pastures.append(pasture)

        return pastures

    # Syötteet

    def click(self, mouse_position: Tuple[float, float]) -> None:
        clicked_pasture = self._get_pasture_in_position(mouse_position)
        if clicked_pasture:
            self._click_on_pasture(clicked_pasture)
        else:
            self._remove_marked_pastures()

    def scroll_up(self) -> None:
        self._add_sheep_to_planned_move()

    def scroll_down(self) -> None:
        self._subtract_sheep_from_planned_move()

    def press_enter(self) -> None:
        self._confirm_move()

    # Vuorot

    def is_in_initial_placement(self) -> bool:
        return self._turn <= 2

    def is_players_turn(self) -> bool:
        return self._is_humans_turn

    def is_computers_turn(self) -> bool:
        return not self._is_humans_turn and not self.is_over_for_ai()

    def next_turn(self) -> None:
        if self._is_humans_turn and not self.is_over_for_ai():
            # Pelaajan vuoro siirtyy tekoälylle, joka ei ole vielä hävinnyt
            self._is_humans_turn = False
        elif not self._is_humans_turn and not self.is_over_for_player():
            # Tekoälyn vuoro siirtyy pelaajalle, joka ei ole vielä hävinnyt
            self._is_humans_turn = True

        self._turn += 1
        self._remove_marked_pastures()

    def _previous_turn(self) -> None:
        self._turn -= 1
        if self.is_in_initial_placement():
            self._is_humans_turn = not self._is_humans_turn
        else:
            if self.is_over_for_player():
                self._is_humans_turn = False
            else:
                self._is_humans_turn = not self._is_humans_turn
        self._remove_marked_pastures()

    # Muuttujien nollaus

    def _remove_planned_sheep(self) -> None:
        for pasture in self.pastures:
            pasture.planned_sheep = None

    def _remove_targets_and_planned_sheep(self) -> None:
        for pasture in self.pastures:
            pasture.targeted = False
            pasture.planned_sheep = None

    def _remove_marked_pastures(self) -> None:
        self.chosen_pasture = None
        self.target_pasture = None
        self._remove_targets_and_planned_sheep()

    # Onko peli ohi?

    def _are_no_potential_moves(self, pastures: List[Pasture]) -> bool:
        for pasture in pastures:
            potential_moves = pasture.get_potential_targets(self.pastures)
            if len(potential_moves) > 0:
                return False
        return True

    def is_over_for_player(self) -> bool:
        if self.is_in_initial_placement():
            return False
        players_pastures = list(filter(
            lambda pasture: pasture.is_occupied_by_player(), self._get_occupied_pastures()))
        return self._are_no_potential_moves(players_pastures)

    def is_over_for_ai(self) -> bool:
        if self.is_in_initial_placement():
            return False
        ais_pastures = list(filter(
            lambda pasture: not pasture.is_occupied_by_player(), self._get_occupied_pastures()))
        return self._are_no_potential_moves(ais_pastures)

    def is_over(self) -> bool:
        if self.is_in_initial_placement():
            return False
        return self._are_no_potential_moves(self._get_occupied_pastures())

    # Laitumet

    def _get_pasture_in_position(self, position: Tuple[float, float]) -> Pasture | None:
        for pasture in self.pastures:
            if pasture.collide_with_point(position):
                return pasture
        return None

    def is_controlled_by_player_in_turn(self, pasture: Pasture) -> bool:
        return self._is_humans_turn == pasture.is_occupied_by_player()

    def _are_pastures_chosen(self) -> bool:
        return self.chosen_pasture is not None and self.target_pasture is not None

    def _get_occupied_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_occupied(), self.pastures))

    def _get_targeted_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.targeted is True, self.pastures))

    def get_amount_of_targeted_pastures(self) -> int:
        return len(self._get_targeted_pastures())

    def get_edge_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_on_edge(self.pastures), self.pastures))

    def get_amount_of_edge_pastures(self) -> int:
        return len(self.get_edge_pastures())

    def _should_be_focused(self, pasture: Pasture, pointed_at: bool) -> bool:
        if pasture is self.chosen_pasture:
            return True
        if pasture.targeted:
            return True
        if pasture.get_amount_of_planned_sheep() > 0:
            return True
        if pointed_at:
            if self.is_in_initial_placement() and pasture.is_on_edge(self.pastures) and pasture.is_free():
                return True
            if not self.is_in_initial_placement() and self.is_controlled_by_player_in_turn(pasture):
                return True
        return False

    def adjust_focus(self, pasture: Pasture, mouse_position: Tuple[float, float]):
        is_pointed_at = pasture.collide_with_point(mouse_position)
        pasture.focused = self._should_be_focused(pasture, is_pointed_at)

    # Siirrot

    def _sheep_can_be_moved(self, pasture: Pasture) -> bool:
        return self.is_controlled_by_player_in_turn(pasture) and pasture.get_amount_of_sheep() > 1 and not pasture.is_surrounded(self.pastures)

    def get_potential_initial_pastures(self) -> List[Pasture]:
        return list(filter(lambda pasture: pasture.is_free() and pasture.is_on_edge(self.pastures), self.pastures))

    def get_potential_sheep_to_move(self) -> List[Pasture]:
        return list(filter(
            self._sheep_can_be_moved, self.pastures))

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
        player = 0 if self._is_humans_turn else 1
        if pasture.is_free() and pasture.is_on_edge(self.pastures):
            pasture.occupy(player, INITIAL_SHEEP)
        else:
            raise ValueError(
                'The given pasture is not suitable for placing sheep.')

    def _add_sheep_to_planned_move(self):
        if self._are_pastures_chosen() and self.chosen_pasture.get_amount_of_planned_sheep() >= 2:
            self.chosen_pasture.subtract_a_planned_sheep()
            self.target_pasture.add_a_planned_sheep()

    def _subtract_sheep_from_planned_move(self):
        if self._are_pastures_chosen() and self.target_pasture.get_amount_of_planned_sheep() >= 2:
            self.chosen_pasture.add_a_planned_sheep()
            self.target_pasture.subtract_a_planned_sheep()

    def _click_on_pasture(self, pasture: Pasture) -> None:
        if self.is_in_initial_placement():
            if pasture.is_on_edge(self.pastures) and not pasture.is_occupied():
                self.make_initial_turn(pasture)
        else:  # Aloituslampaat on jo asetettu
            if pasture.is_occupied() and self.is_controlled_by_player_in_turn(pasture):
                # Valitaan lähtöruutu
                self.chosen_pasture = pasture
                if self.target_pasture is not None:
                    self._remove_planned_sheep()
                    self.target_pasture = None
                targets = pasture.get_potential_targets(
                    self.pastures)
                for p in self.pastures:
                    p.targeted = p in targets
            elif pasture.targeted and self.chosen_pasture is not None and self.chosen_pasture.get_amount_of_sheep() > 0 and pasture is not self.chosen_pasture:
                # Jos lähtöruutu valittu, valitaan kohderuutu
                if self.target_pasture is not None:
                    self._remove_planned_sheep()
                self.target_pasture = pasture
                pasture.planned_sheep = 1
                self.chosen_pasture.planned_sheep = self.chosen_pasture.get_amount_of_sheep() - 1
            else:
                self._remove_marked_pastures()

    def _confirm_move(self):
        if self._are_pastures_chosen() and self.chosen_pasture.get_amount_of_planned_sheep() > 0 and self.target_pasture.get_amount_of_planned_sheep() > 0:
            self._move_sheep()
            self.next_turn()

    def make_initial_turn(self, pasture: Pasture) -> None:
        self._place_initial_sheep(pasture)
        self.next_turn()

    def undo_initial_move(self, pasture: Pasture) -> None:
        pasture.reset()
        self._previous_turn()

    def make_normal_turn(self, pasture: Pasture, target: Pasture, sheep: int) -> None:
        pasture.planned_sheep = pasture.get_amount_of_sheep() - sheep
        target.planned_sheep = target.get_amount_of_sheep() + sheep

        self.chosen_pasture = pasture
        self.target_pasture = target

        self._move_sheep()
        self.next_turn()

    def undo_move(self, pasture: Pasture, target_pasture: Pasture, sheep: int) -> None:
        if pasture.occupier is None:
            raise ValueError('Pasture occupier not found')
        pasture.occupy(
            pasture.occupier, pasture.get_amount_of_sheep() + sheep)
        target_pasture.reset()
        self._previous_turn()

    # Heuristiikka ja voittajan laskenta

    def evaluate_game_state(self) -> float:
        # Palautetaan paras tai huonoin mahdollinen arvo voittajan mukaan, mikäli peli on ohi
        if self.is_over():
            if self._calculate_human_won():
                return float('Inf')
            return float('-Inf')

        value: float = 0
        for pasture in self._get_occupied_pastures():
            sheep = pasture.get_amount_of_sheep()
            is_surrounded = pasture.is_surrounded(self.pastures)
            free_neighbours = pasture.get_amount_of_free_neighbours(
                self.pastures)
            friendly_neighbours = pasture.get_amount_of_friendly_neighbours(
                self.pastures)
            if pasture.is_occupied_by_player():
                # Jokaisesta tyhjästä naapurilaitumesta piste kerrottuna lampaiden määrällä
                value += free_neighbours * sheep
                # Kymmenesosapiste jokaisesta omasta naapurilaitumesta
                value += friendly_neighbours * 0.1
                if is_surrounded:
                    # Jokaisesta ansaan jääneestä lampaasta miinuspiste
                    value -= sheep
            else:
                value -= free_neighbours * sheep
                value -= friendly_neighbours * 0.01
                if is_surrounded:
                    value += sheep
        return value

    def _human_has_larger_continuous_pasture(self) -> bool:
        # Toteutus vaatii vielä parantelua
        human_friendly_neighbours = 0
        ai_friendly_neighbours = 0
        for pasture in self.pastures:
            friendly_neighbours = pasture.get_amount_of_friendly_neighbours(
                self.pastures)
            if pasture.is_occupied_by_player():
                human_friendly_neighbours += friendly_neighbours
            else:
                ai_friendly_neighbours += friendly_neighbours
        return human_friendly_neighbours > ai_friendly_neighbours

    def _calculate_human_won(self) -> bool:
        human_points = 0
        ai_points = 0
        for pasture in self.pastures:
            if pasture.is_occupied():
                if pasture.is_occupied_by_player():
                    human_points += 1
                else:
                    ai_points += 1
        if human_points == ai_points:
            return self._human_has_larger_continuous_pasture()
        return human_points > ai_points

    def get_info_text(self) -> str:
        if self.is_over():
            if self._calculate_human_won():
                return 'Pelaaja voitti!'
            return 'Tekoäly voitti!'
        if self.is_players_turn():
            return 'Pelaajan vuoro'
        return 'Tekoälyn vuoro'
