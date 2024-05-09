from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Tuple
from constants import (
    COMPUTER,
    DIRECTION_VECTORS,
    HALF_RADIUS,
    MINIMAL_RADIUS,
    PASTURE_RADIUS,
    PLAYER
)


@dataclass
class Pasture:
    position: Tuple[float, float]
    occupier: int | None = None
    sheep: int | None = None
    planned_sheep: int | None = None
    is_targeted: bool = False

    def __post_init__(self):
        self.vertices = self._compute_vertices()

    def _compute_vertices(self) -> List[Tuple[float, float]]:
        """Palauttaa listan laitumen kärjistä koordinaattipareina"""
        x, y = self.position
        return [
            (x, y),
            (x - HALF_RADIUS, y + MINIMAL_RADIUS),
            (x, y + 2 * MINIMAL_RADIUS),
            (x + PASTURE_RADIUS, y + 2 * MINIMAL_RADIUS),
            (x + 3 * HALF_RADIUS, y + MINIMAL_RADIUS),
            (x + PASTURE_RADIUS, y),
        ]

    @property
    def centre(self) -> Tuple[float, float]:
        """Palauttaa laitumen keskipisteen"""
        x, y = self.position
        return (x + HALF_RADIUS, y + MINIMAL_RADIUS)

    # Laitumen lampaat ja valtaus

    def is_occupied(self) -> bool:
        """Palauttaa tosi, jos laidun on miehitetty"""
        return self.occupier is not None

    def is_occupied_by_player(self) -> bool:
        """Palauttaa tosi, jos laidun on pelaajan miehittämä"""
        return self.occupier == PLAYER

    def is_occupied_by_computer(self) -> bool:
        """Palauttaa tosi, jos laidun on tekoälyn miehittämä"""
        return self.occupier == COMPUTER

    def is_free(self) -> bool:
        """Palauttaa tosi, jos laidun on vapaa"""
        return self.occupier is None

    def get_amount_of_sheep(self) -> int:
        """Palauttaa lampaiden määrän"""
        return self.sheep if self.sheep is not None else 0

    def get_amount_of_planned_sheep(self) -> int:
        """Palauttaa suunniteltujen lampaiden määrän"""
        return self.planned_sheep if self.planned_sheep is not None else 0

    def change_planned_sheep(self, change: int):
        """Lisää tai vähentää annetun määrän lampaita"""
        self.planned_sheep = self.get_amount_of_planned_sheep() + change

    def occupy(self, occupier: int, sheep: int) -> None:
        """Miehittää laitumen annetulla lammasmäärällä"""
        self.occupier = occupier
        self.sheep = sheep

    def reset(self) -> None:
        """Tyhjentää laitumen tiedot"""
        self.occupier = None
        self.sheep = None
        self.planned_sheep = None
        self.is_targeted = False

    def get_value(self, pastures: List[Pasture]) -> int:
        """Palauttaa laitumen heuristisen arvon"""
        sheep_able_to_move = self.get_amount_of_sheep() - 1
        if sheep_able_to_move < 1:
            return 0

        potential_targets = self.get_amount_of_potential_targets(
            pastures)
        if potential_targets < 1:
            return 0

        amount_of_possible_moves = sheep_able_to_move * potential_targets
        if self.is_occupied_by_player():
            return amount_of_possible_moves
        return -amount_of_possible_moves

        # Laitumen naapurit

    def _is_neighbour(self, pasture: Pasture) -> bool:
        """Palauttaa tosi, jos annettu laidun on naapuri"""
        distance = math.dist(pasture.centre, self.centre)
        return math.isclose(distance, 2 * MINIMAL_RADIUS, rel_tol=0.05)

    def get_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        """Palauttaa kaikki naapurilaitumet"""
        return [pasture for pasture in pastures if self._is_neighbour(pasture)]

    def _get_amount_of_neighbours(self, pastures: List[Pasture]) -> int:
        """Palauttaa naapurilaitumien määrän"""
        return len(self.get_neighbours(pastures))

    def is_on_edge(self, pastures: List[Pasture]) -> bool:
        """Palauttaa tosi, jos laidun on pelilaudan reunalla"""
        return self._get_amount_of_neighbours(pastures) < 6

    def is_potential_initial_pasture(self, pastures: List[Pasture]) -> bool:
        """Palauttaa tosi, jos laidun on mahdollinen aloituslaidun"""
        return self.is_free() and self.is_on_edge(pastures)

    def get_free_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        """Palauttaa vapaat naapurilaitumet"""
        return list(filter(lambda n: n.is_free(), self.get_neighbours(pastures)))

    def _get_amount_of_free_neighbours(self, pastures: List[Pasture]) -> int:
        """Palauttaa vapaiden naapurilaitumien määrän"""
        return len(self.get_free_neighbours(pastures))

    def is_surrounded(self, pastures: List[Pasture]) -> bool:
        """Palauttaa tosi, jos laidun on ympäröity miehitetyillä laitumilla"""
        return self._get_amount_of_free_neighbours(pastures) == 0

    def is_possible_to_move(self, pastures: List[Pasture]) -> bool:
        """Palauttaa tosi, jos lampaita voi siirtää"""
        return self.get_amount_of_sheep() > 1 and not self.is_surrounded(pastures)

    # Pelimekaniikka

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Palauttaa tosi, jos annettu positio on laitumella"""
        return math.dist(point, self.centre) < MINIMAL_RADIUS

    def _get_pasture_at_point(self, vector: Tuple[float, float],
                              distance: int, pastures: List[Pasture]) -> Pasture | None:
        """Palauttaa laitumen annetusta positiosta, jos sellainen löytyy annetuista laitumista"""
        target_position = (self.centre[0] + vector[0] * distance,
                           self.centre[1] + vector[1] * distance)

        for pasture in pastures:
            if (math.isclose(pasture.centre[0], target_position[0], rel_tol=0.05)
                    and math.isclose(pasture.centre[1], target_position[1], rel_tol=0.05)):
                return pasture
        return None

    def _get_target_pasture(self, vector: Tuple[float, float],
                            pastures: List[Pasture]) -> Pasture | None:
        """Palauttaa viimeisen vapaan laitumen annetusta suunnasta, jos sellainen löytyy"""
        current_distance = 1
        while True:
            potential_target = self._get_pasture_at_point(
                vector, current_distance, pastures)
            if potential_target is None or potential_target.is_occupied():
                # Palauttaa edellisen laitumen, mikäli laidun on vallattu
                # tai pelilaudan reuna tullut vastaan.
                if current_distance < 2:
                    # Ei palauteta lähtöruutua, mikäli ei päästy yhtä laidunta kauemmaksi.
                    return None
                last_valid_pasture = self._get_pasture_at_point(
                    vector, current_distance - 1, pastures)
                return last_valid_pasture
            current_distance += 1

    def get_potential_targets(self, pastures: List[Pasture]) -> List[Pasture]:
        """Palauttaa mahdolliset kohteet annetuista laitumista"""
        potential_targets: List[Pasture] = []
        for vector in DIRECTION_VECTORS:
            target_pasture = self._get_target_pasture(vector, pastures)
            if target_pasture is not None:
                potential_targets.append(target_pasture)
        return potential_targets

    def get_amount_of_potential_targets(self, pastures: List[Pasture]) -> int:
        """Palauttaa mahdollisten kohteiden määrän annetuista laitumista"""
        return len(self.get_potential_targets(pastures))

    def get_any_potential_target(self, pastures: List[Pasture]) -> Pasture | None:
        """Palauttaa minkä tahansa mahdollisen kohdelaitumen, jos sellainen löytyy"""
        if not self.is_possible_to_move(pastures):
            return None
        for vector in DIRECTION_VECTORS:
            target_pasture = self._get_target_pasture(vector, pastures)
            if target_pasture is not None:
                return target_pasture
        return None

    def are_any_potential_targets(self, pastures: List[Pasture]) -> bool:
        """Palauttaa tosi, jos annetuista laitumista löytyy yksikin mahdollinen kohde"""
        if not self.is_possible_to_move(pastures):
            return False
        for vector in DIRECTION_VECTORS:
            if self._get_target_pasture(vector, pastures) is not None:
                return True
        return False
