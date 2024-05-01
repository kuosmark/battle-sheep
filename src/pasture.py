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

    def __eq__(self, other):
        return self.position == other.position and self.occupier == other.occupier and self.sheep == other.sheep

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
        return self.occupier is not None

    def is_occupied_by_player(self) -> bool:
        return self.occupier == PLAYER

    def is_occupied_by_computer(self) -> bool:
        return self.occupier == COMPUTER

    def is_free(self) -> bool:
        return self.occupier is None

    def get_amount_of_sheep(self) -> int:
        return self.sheep if self.sheep is not None else 0

    def get_amount_of_planned_sheep(self) -> int:
        return self.planned_sheep if self.planned_sheep is not None else 0

    def add_a_planned_sheep(self):
        self.planned_sheep = self.get_amount_of_planned_sheep() + 1

    def subtract_a_planned_sheep(self):
        self.planned_sheep = self.get_amount_of_planned_sheep() - 1

    def occupy(self, occupier: int, sheep: int) -> None:
        self.occupier = occupier
        self.sheep = sheep

    def reset(self) -> None:
        self.occupier = None
        self.sheep = None
        self.planned_sheep = None
        self.is_targeted = False

    def get_value(self, pastures: List[Pasture]) -> int:
        different_moves_possible = self.get_amount_of_possible_targets(
            pastures) * self.get_amount_of_sheep() - 1
        if self.is_occupied_by_player():
            return different_moves_possible
        return -abs(different_moves_possible)

        # Laitumen naapurit

    def _is_neighbour(self, pasture: Pasture) -> bool:
        """Palauttaa, onko laidun naapuri"""
        distance = math.dist(pasture.centre, self.centre)
        return math.isclose(distance, 2 * MINIMAL_RADIUS, rel_tol=0.05)

    def get_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        """Palauttaa kaikki naapurilaitumet"""
        return [pasture for pasture in pastures if self._is_neighbour(pasture)]

    def _get_amount_of_neighbours(self, pastures: List[Pasture]) -> int:
        """Palauttaa naapurilaitumien määrän"""
        return len(self.get_neighbours(pastures))

    def is_on_edge(self, pastures: List[Pasture]) -> bool:
        """Kertoo, onko laidun pelilaudan reunalla (reunalaitumilla on alle 6 naapuria)"""
        return self._get_amount_of_neighbours(pastures) < 6

    def is_potential_initial_pasture(self, pastures: List[Pasture]) -> bool:
        """Kertoo, onko laidun potentiaalinen aloituslaidun"""
        return self.is_free() and self.is_on_edge(pastures)

    def get_free_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        return list(filter(lambda n: n.is_free(), self.get_neighbours(pastures)))

    def get_amount_of_free_neighbours(self, pastures: List[Pasture]) -> int:
        return len(self.get_free_neighbours(pastures))

    def is_surrounded(self, pastures: List[Pasture]) -> bool:
        """Palauttaa, onko laidun ympäröity vallatuilla laitumilla"""
        return self.get_amount_of_free_neighbours(pastures) == 0

    def is_possible_to_move(self, pastures: List[Pasture]) -> bool:
        """Palauttaa, voiko laitumelta siirtää lampaita"""
        return self.get_amount_of_sheep() > 1 and not self.is_surrounded(pastures)

    def is_friendly(self, pasture: Pasture) -> bool:
        """Palauttaa, onko laitumella sama miehittäjä"""
        return self.occupier is not None and self.occupier == pasture.occupier

    def _get_friendly_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        return list(filter(self.is_friendly, self.get_neighbours(pastures)))

    def get_amount_of_friendly_neighbours(self, pastures: List[Pasture]) -> int:
        return len(self._get_friendly_neighbours(pastures))

    # Pelimekaniikka

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < MINIMAL_RADIUS

    def _get_pasture_at_direction_and_distance(self, vector, current_distance, pastures) -> Pasture | None:
        """Etsii laitumen annetusta suunnasta, annetun etäisyyden päästä."""
        target_position = (self.centre[0] + vector[0] * current_distance,
                           self.centre[1] + vector[1] * current_distance)

        for pasture in pastures:
            if math.isclose(pasture.centre[0], target_position[0], rel_tol=0.05) and math.isclose(
                    pasture.centre[1], target_position[1], rel_tol=0.05):
                return pasture
        return None

    def _get_target_pasture(self, vector: Tuple[float, float], pastures: List[Pasture]) -> Pasture | None:
        """Etsii viimeisen vapaan laitumen annetusta suunnasta."""
        current_distance = 1
        while True:
            potential_target = self._get_pasture_at_direction_and_distance(
                vector, current_distance, pastures)
            if potential_target is None or potential_target.is_occupied():
                # Palauttaa edellisen laitumen, mikäli laidun on vallattu
                # tai pelilaudan reuna tullut vastaan.
                if current_distance < 2:
                    # Ei palauteta lähtöruutua, mikäli ei päästy yhtä laidunta kauemmaksi.
                    return None
                last_valid_pasture = self._get_pasture_at_direction_and_distance(
                    vector, current_distance - 1, pastures)
                return last_valid_pasture
            current_distance += 1

    def get_potential_targets(self, pastures: List[Pasture]) -> List[Pasture]:
        potential_targets: List[Pasture] = []
        for vector in DIRECTION_VECTORS:
            target_pasture = self._get_target_pasture(vector, pastures)
            if target_pasture is not None:
                potential_targets.append(target_pasture)
        return potential_targets

    def get_amount_of_possible_targets(self, pastures: List[Pasture]) -> int:
        return len(self.get_potential_targets(pastures))

    def get_any_potential_target(self, pastures: List[Pasture]) -> Pasture | None:
        if not self.is_possible_to_move(pastures):
            return None
        for vector in DIRECTION_VECTORS:
            target_pasture = self._get_target_pasture(vector, pastures)
            if target_pasture is not None:
                return target_pasture
        return None

    def are_any_potential_targets(self, pastures: List[Pasture]) -> bool:
        if not self.is_possible_to_move(pastures):
            return False
        for vector in DIRECTION_VECTORS:
            if self._get_target_pasture(vector, pastures) is not None:
                return True
        return False
