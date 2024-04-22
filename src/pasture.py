from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

import pygame

PASTURE_COLOR = (163, 178, 3)  # vaalea ruoho
RED_SHEEP_COLOR = (206, 51, 27)
BLUE_SHEEP_COLOR = (7, 83, 141)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PASTURE_RADIUS = 50
HIGHLIGHT_OFFSET = 60
MAX_SHEEP = 16
MIN_SHEEP = 1


@dataclass
class Pasture:
    position: Tuple[float, float]
    sheep: int | None = None
    planned_sheep: int | None = None
    occupier: int | None = None
    targeted: bool = False
    color: Tuple[int, int, int] = PASTURE_COLOR
    focused = False

    def __post_init__(self):
        self.vertices = self.compute_vertices()

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Palauttaa listan laitumen kärjistä koordinaattipareina"""
        x, y = self.position
        half_radius = PASTURE_RADIUS / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + PASTURE_RADIUS, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + PASTURE_RADIUS, y),
        ]

    @property
    def minimal_radius(self) -> float:
        """Palauttaa laitumen minimisäteen"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return PASTURE_RADIUS * math.cos(math.radians(30))

    @property
    def centre(self) -> Tuple[float, float]:
        """Palauttaa laitumen keskipisteen"""
        x, y = self.position
        return (x + PASTURE_RADIUS / 2, y + self.minimal_radius)

    @property
    def highlight_color(self) -> Tuple[int, ...]:
        """color of the pasture tile when rendering highlight"""
        offset = HIGHLIGHT_OFFSET if self.focused else 0

        def brighten(x, y):
            return x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.color)

    # Laitumen lampaat ja valtaus

    def is_occupied(self) -> bool:
        return self.occupier is not None

    def is_occupied_by_player(self) -> bool:
        return self.occupier == 0

    def is_free(self) -> bool:
        return self.occupier is None

    def get_amount_of_sheep(self) -> int:
        return self.sheep if self.sheep is not None else 0

    def get_amount_of_planned_sheep(self) -> int:
        return self.planned_sheep if self.planned_sheep is not None else 0

    def add_a_sheep(self):
        self.planned_sheep = self.planned_sheep + 1

    # def add_planned_sheep(self, amount: int):
    #     planned_sheep = self.get_amount_of_planned_sheep() + amount
    #     if planned_sheep > MAX_SHEEP:
    #         raise ValueError('Invalid amount of sheep planned')
    #     self.planned_sheep = planned_sheep

    # def subtract_planned_sheep(self, amount: int):
    #     planned_sheep = self.get_amount_of_planned_sheep() - amount
    #     if planned_sheep < MIN_SHEEP:
    #         raise ValueError('Invalid amount of sheep planned')
    #     self.planned_sheep = planned_sheep

    def deduct_a_sheep(self):
        self.planned_sheep = self.planned_sheep - 1

    def update_sheep(self, occupier: int, new_amount: int) -> None:
        self.occupier = occupier
        if occupier == 0:
            self.color = RED_SHEEP_COLOR
        elif occupier == 1:
            self.color = BLUE_SHEEP_COLOR
        self.sheep = new_amount

    def move_sheep_to(self, target_pasture: Pasture) -> None:
        """Siirtää suunnitellut lampaat annetulle laitumelle."""
        if self.occupier is not None and target_pasture.planned_sheep is not None and self.planned_sheep is not None:
            target_pasture.update_sheep(
                self.occupier, target_pasture.planned_sheep)
            self.update_sheep(self.occupier, self.planned_sheep)
            self.planned_sheep = None
            target_pasture.planned_sheep = None

    def move_amount_of_sheep_to(self, target_pasture: Pasture, sheep: int) -> None:
        if self.occupier is not None:
            target_pasture.update_sheep(
                self.occupier, sheep)
            new_amount = self.get_amount_of_sheep() - sheep
            self.update_sheep(self.occupier, new_amount)

    def reset(self) -> None:
        self.sheep = None
        self.planned_sheep = None
        self.occupier = None
        self.targeted = False
        self.color = PASTURE_COLOR
        self.focused = False

    # Laitumen naapurit

    def is_neighbour(self, pasture: Pasture) -> bool:
        """Palauttaa, onko laidun naapuri"""
        distance = math.dist(pasture.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def get_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        """Palauttaa kaikki naapurilaitumet"""
        return [pasture for pasture in pastures if self.is_neighbour(pasture)]

    def get_number_of_neighbours(self, pastures: List[Pasture]) -> int:
        """Palauttaa naapurilaitumien määrän"""
        return len(self.get_neighbours(pastures))

    def is_on_edge(self, pastures: List[Pasture]) -> bool:
        """Kertoo, onko laidun pelilaudan reunalla (reunalaitumilla on alle 6 naapuria)"""
        return self.get_number_of_neighbours(pastures) < 6

    def get_free_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        neighbours = self.get_neighbours(pastures)
        return list(filter(lambda n: n.is_free(), neighbours))

    def get_amount_of_free_neighbours(self, pastures: List[Pasture]) -> int:
        return len(self.get_free_neighbours(pastures))

    def is_surrounded(self, pastures: List[Pasture]) -> bool:
        """Palauttaa, onko laidun ympäröity vallatuilla laitumilla"""
        return self.get_amount_of_free_neighbours(pastures) == 0

    def is_friendly(self, pasture: Pasture) -> bool:
        """Palauttaa, onko laitumella sama miehittäjä"""
        return self.occupier == pasture.occupier

    def get_friendly_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        return list(filter(self.is_friendly, self.get_neighbours(pastures)))

    def get_amount_of_friendly_neighbours(self, pastures: List[Pasture]) -> int:
        return len(self.get_friendly_neighbours(pastures))

    # Pelimekaniikka

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def get_all_direction_vectors(self):
        """Returns all direction vectors for a flat-topped hex grid."""
        direction_vectors = {
            "N": (0, -2 * self.minimal_radius),
            "S": (0, 2 * self.minimal_radius),
            "NE": (math.sqrt(3) * self.minimal_radius, -(self.minimal_radius)),
            "NW": (-(math.sqrt(3) * self.minimal_radius), -(self.minimal_radius)),
            "SE": (math.sqrt(3) * self.minimal_radius, self.minimal_radius),
            "SW": (-(math.sqrt(3) * self.minimal_radius), self.minimal_radius),
        }
        return direction_vectors

    def get_pasture_at_direction_and_distance(self, vector, current_distance, pastures) -> Pasture | None:
        """Etsii laitumen annetusta suunnasta, annetun etäisyyden päästä."""

        target_position = (self.centre[0] + vector[0] * current_distance,
                           self.centre[1] + vector[1] * current_distance)

        for pasture in pastures:
            if math.isclose(pasture.centre[0], target_position[0], rel_tol=0.05) and math.isclose(
                    pasture.centre[1], target_position[1], rel_tol=0.05):
                return pasture
        return None

    def get_target_pasture(self, vector: Tuple[int, int], pastures: List[Pasture]) -> Pasture | None:
        """Etsii viimeisen vapaan laitumen annetusta suunnasta."""
        current_distance = 1
        while True:
            potential_target = self.get_pasture_at_direction_and_distance(
                vector, current_distance, pastures)
            if potential_target is None or potential_target.is_occupied():
                # Palauttaa edellisen laitumen, mikäli laidun on vallattu
                # tai pelilaudan reuna tullut vastaan.
                if current_distance < 2:
                    # Ei palauteta lähtöruutua, mikäli ei päästy yhtä laidunta kauemmaksi.
                    return None
                last_valid_pasture = self.get_pasture_at_direction_and_distance(
                    vector, current_distance - 1, pastures)
                return last_valid_pasture
            current_distance += 1

    def get_potential_targets(self, pastures: List[Pasture]) -> List[Pasture]:
        if self.is_surrounded(pastures) or self.sheep is None or self.sheep < 2:
            return []
        potential_targets: List[Pasture] = []
        directions = self.get_all_direction_vectors()
        for vector in directions.values():
            target_pasture = self.get_target_pasture(vector, pastures)
            if target_pasture is not None:
                potential_targets.append(target_pasture)
        return potential_targets

    def render(self, screen, font) -> None:
        """Piirtää laitumen näytölle"""
        pygame.draw.polygon(screen, self.highlight_color, self.vertices)
        if self.planned_sheep is not None:
            text_surface = font.render(
                str(self.planned_sheep), True, BLACK)
            text_rect = text_surface.get_rect(center=self.centre)
            screen.blit(text_surface, text_rect)
        elif self.sheep is not None:
            text_surface = font.render(str(self.sheep), True, WHITE)
            text_rect = text_surface.get_rect(center=self.centre)
            screen.blit(text_surface, text_rect)
