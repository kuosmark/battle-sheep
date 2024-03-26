from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List
from typing import Tuple
from uuid import uuid4

import pygame

PASTURE_COLOR = (163, 178, 3)  # vaalea ruoho
RED_SHEEP_COLOR = (206, 51, 27)  # punainen
BLUE_SHEEP_COLOR = (7, 83, 141)  # sininen
TEXT_COLOR = (0, 0, 0)  # musta


@dataclass
class Pasture:
    position: Tuple[float, float]
    sheep: int | None = None
    owner: int | None = None
    colour: Tuple[int, ...] = PASTURE_COLOR
    radius: float = 50
    highlight_offset: int = 3
    max_highlight_ticks: int = 15
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        self.vertices = self.compute_vertices()
        self.highlight_tick = 0

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1

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

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, pasture: Pasture) -> bool:
        """Returns True if pasture centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(pasture.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def render(self, screen, font) -> None:
        """Piirtää laitumen näytölle"""
        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        if self.sheep is not None:
            text_surface = font.render(str(self.sheep), True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=self.centre)
            screen.blit(text_surface, text_rect)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the pasture with the specified colour"""
        self.highlight_tick = self.max_highlight_ticks
        pygame.draw.aalines(screen, border_colour,
                            closed=True, points=self.vertices)

    def is_taken(self) -> bool:
        return self.owner is not None

    def update_sheep(self, owner: int, new_amount: int) -> None:
        self.owner = owner
        if owner == 0:
            self.colour = RED_SHEEP_COLOR
        elif owner == 1:
            self.colour = BLUE_SHEEP_COLOR
        self.sheep = new_amount

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
        offset = self.highlight_offset * self.highlight_tick

        def brighten(x, y):
            return x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)
