from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

import pygame

PASTURE_COLOR = (163, 178, 3)  # vaalea ruoho
RED_SHEEP_COLOR = (206, 51, 27)  # punainen
BLUE_SHEEP_COLOR = (7, 83, 141)  # sininen
BLACK = (0, 0, 0)  # musta
WHITE = (255, 255, 255)  # valkoinen


@dataclass
class Pasture:
    position: Tuple[float, float]
    sheep: int | None = None
    planned_sheep: int | None = None
    owner: int | None = None
    targeted: bool = False
    colour: Tuple[int, ...] = PASTURE_COLOR
    radius: float = 50
    focused = False

    def __post_init__(self):
        self.vertices = self.compute_vertices()

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the pasture's vertices as x, y tuples"""
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius, y),
        ]

    def compute_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        """Returns pastures whose centres are two minimal radiuses away from self.centre"""
        return [pasture for pasture in pastures if self.is_neighbour(pasture)]

    def number_of_neighbours(self, pastures: List[Pasture]) -> int:
        """Palauttaa laitumen naapurilaitumien määrän"""
        neighbours = self.compute_neighbours(pastures)
        return len(neighbours)

    def is_on_edge(self, pastures: List[Pasture]) -> bool:
        """Kertoo, onko laidun pelilaudan reunalla (reunalaitumilla on alle 6 naapuria)"""
        return self.number_of_neighbours(pastures) < 6

    def get_amount_of_sheep(self) -> int:
        return self.sheep if self.sheep is not None else 0

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, pasture: Pasture) -> bool:
        """Returns True if pasture centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(pasture.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def has_free_neighbour(self, pasture: Pasture) -> bool:
        """Kertoo, onko laidun naapuri ja vapaana"""
        return self.is_neighbour(pasture) and not pasture.is_taken()

    def get_free_neighbours(self, pastures: List[Pasture]) -> List[Pasture]:
        """Palauttaa vapaat naapurilaitumet"""
        return list(filter(self.has_free_neighbour, pastures))

    def is_surrounded(self, pastures: List[Pasture]) -> bool:
        """Palauttaa, onko laidun ympäröity vallatuilla laitumilla"""
        free_neighbours = self.get_free_neighbours(pastures)
        return len(free_neighbours) == 0

    def render(self, screen, font) -> None:
        """Piirtää laitumen näytölle"""
        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        if self.planned_sheep is not None:
            text_surface = font.render(
                str(self.planned_sheep), True, BLACK)
            text_rect = text_surface.get_rect(center=self.centre)
            screen.blit(text_surface, text_rect)
        elif self.sheep is not None:
            text_surface = font.render(str(self.sheep), True, WHITE)
            text_rect = text_surface.get_rect(center=self.centre)
            screen.blit(text_surface, text_rect)

    def is_taken(self) -> bool:
        return self.owner is not None

    def is_free(self) -> bool:
        return self.owner is None

    def add_a_sheep(self):
        self.planned_sheep = self.planned_sheep + 1

    def deduct_a_sheep(self):
        self.planned_sheep = self.planned_sheep - 1

    def is_owned_by_human(self):
        return self.owner == 0

    def update_sheep(self, owner: int, new_amount: int) -> None:
        self.owner = owner
        if owner == 0:
            self.colour = RED_SHEEP_COLOR
        elif owner == 1:
            self.colour = BLUE_SHEEP_COLOR
        self.sheep = new_amount

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

    def move_sheep_to(self, target_pasture: Pasture) -> None:
        """Siirtää kaikki paitsi yhden lampaista annetulle laitumelle."""
        if self.owner is not None and target_pasture.planned_sheep is not None and self.planned_sheep is not None:
            target_pasture.update_sheep(
                self.owner, target_pasture.planned_sheep)
            self.update_sheep(self.owner, self.planned_sheep)
            self.planned_sheep = None
            target_pasture.planned_sheep = None

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
            if potential_target is None or potential_target.is_taken():
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

    @property
    def centre(self) -> Tuple[float, float]:
        """Palauttaa laitumen keskipisteen"""
        x, y = self.position
        return (x + self.radius / 2, y + self.minimal_radius)

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the pasture"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Colour of the pasture tile when rendering highlight"""
        offset = 60 if self.focused else 0

        def brighten(x, y):
            return x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)
