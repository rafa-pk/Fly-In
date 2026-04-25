from typing import Any
from dataclasses import dataclass 
from graph_classes import Graph
from math import pi, cos, sin
import pygame


@dataclass
class Drone:
    id: str
    origin: str
    destination: str
    priority: int
    path: list[tuple[str, float]]
    status: str = "idle"

    def get_pos(self, frac_t: float, graph: Graph) -> tuple[float, float]:
        if not self.path:
            start = graph.nodes[self.origin]
            return start.x, start.y
        if frac_t <= self.path[0][1]:
            start = graph.nodes[self.path[0][0]]
            return start.x, start.y
        if frac_t >= self.path[-1][1]:
            end = graph.nodes[self.path[-1][0]]
            return end.x, end.y
        for i in range(len(self.path) - 1):
            pos1, t1 = self.path[i]
            pos2, t2 = self.path[i + 1]
            pos1 = graph.nodes[pos1]
            pos2 = graph.nodes[pos2]
            if t1 <= frac_t <= t2:
                progress = (frac_t - t1) / (t2 - t1)
                x = pos1.x + (pos2.x - pos1.x) * progress
                y = pos1.y + (pos2.y - pos1.y) * progress
        return x, y


class HeapQueue:

    def __init__(self) -> None:
        self._data = []

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._data[parent] <= self._data[i]:
                break
            self._data[parent], self._data[i] = \
                self._data[i], self._data[parent]
            i = parent 

    def _sift_down(self, i: int) -> None:
        length = len(self._data)
        while True:
            smallest = i
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            if (left_child < length and
               self._data[left_child] < self._data[smallest]):
                smallest = left_child
            if (right_child < length and
               self._data[right_child] < self._data[smallest]):
                smallest = right_child
            if smallest == i:
                break
            self._data[i], self._data[smallest] = \
                self._data[smallest], self._data[i]
            i = smallest

    def push(self, value: int) -> None:
        if not value:
            raise ValueError("Push needs a value, cannot push empty value")
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> int:
        if not self._data:
            raise ValueError("Attempt to pop from empty heap")
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        min = self._data.pop()
        if self._data:
            self._sift_down(0)
        return min

    def peek(self) -> int:
        return self.data[0]

    def heapify(self, array: list[Any]) -> None:
        self._data = list(array)
        for i in range(len(array) // 2 - 1, -1, -1):
            self._sift_down(i)

    def __bool__(self) -> bool:
        return bool(self._data) 

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"HeapQueue({self._data})"


class Utils:

    @staticmethod
    def init_drones(graph: Graph) -> list[Drone]:
        return [Drone(id=f"D{i}",
                      origin=graph.start.name,
                      destination=graph.end.name,
                      priority=i,
                      path=[])
                for i in range(graph.nb_drones)]

    @staticmethod
    def draw_text(screen, text: str, font: str, color: tuple[int, int, int],
                  x: int, y: int) -> None:
        """method to draw text to screen"""
        image = font.render(text, True, color)
        screen.blit(image, (x, y))
    
    @staticmethod
    def draw_text_box(screen, text: str, text_color: tuple[int, int, int], 
                      font: str, bg_color: tuple[int, int, int],
                      x: int, y: int, padding: int) -> None:
        """method to draw text to screen with bg underneath"""
        image = font.render(text, True, text_color)
        text_box = image.get_rect(topleft=(x,y))
        bg_rect = pygame.Rect(text_box.x - padding, text_box.y - padding, 
                              text_box.width + padding*2, text_box.height + padding*2)
        pygame.draw.rect(screen, bg_color, bg_rect, 0)
        screen.blit(image, (x, y))

    @staticmethod
    def drone_offset(index: int, total_drones: int) -> tuple[float, float]:
        radius = 5
        if total_drones <= 1:
            return 0.0, 0.0
        angle = 2 * pi * index / total_drones
        return radius * cos(angle), radius * sin(angle)
