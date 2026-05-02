from typing import Any
from dataclasses import dataclass
from graph_classes import Graph
from math import pi, cos, sin
import pygame


@dataclass
class Drone:
    """Drone data class, defines drone attrs"""
    id: str
    origin: str
    destination: str
    priority: int
    path: list[tuple[str, int]]
    status: str = "idle"

    def get_pos(self, frac_t: float, graph: Graph) -> tuple[float, float]:
        """
        Get drone position at fractional time-frame between nodes, so that the
        visualization runs smoothly.

        Parameters:
        frac_t(float): fractional time-frame the drone is at
        graph(Graph): graph instance to access attributes

        Returns:
        tuple[float, float]: coordinates after having found them with the
        formula
        """
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
            ob_pos1 = graph.nodes[pos1]
            ob_pos2 = graph.nodes[pos2]
            if t1 <= frac_t <= t2:
                progress = (frac_t - t1) / (t2 - t1)
                x = ob_pos1.x + (ob_pos2.x - ob_pos1.x) * progress
                y = ob_pos1.y + (ob_pos2.y - ob_pos1.y) * progress
        return x, y


class HeapQueue:
    """Custom MinHeap implementation, mimics heapq module"""
    def __init__(self) -> None:
        """Initialization method, defines underlying list"""
        self._data: list[Any] = []

    def _sift_up(self, i: Any) -> None:
        """Makes given value sift to the top of the binary tree"""
        while i > 0:
            parent = (i - 1) // 2
            if self._data[parent] <= self._data[i]:
                break
            self._data[parent], self._data[i] = \
                self._data[i], self._data[parent]
            i = parent

    def _sift_down(self, i: Any) -> None:
        """Makes given value sift downwards to place in the binary tree"""
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

    def push(self, value: Any) -> None:
        """Push method, appends value and moves it to the right place"""
        if not value:
            raise ValueError("Push needs a value, cannot push empty value")
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> Any:
        """pops smallest value and rearranges heap"""
        if not self._data:
            raise ValueError("Attempt to pop from empty heap")
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        min = self._data.pop()
        if self._data:
            self._sift_down(0)
        return min

    def peek(self) -> Any:
        """Returns value of index-0 element"""
        return self._data[0]

    def heapify(self, array: list[Any]) -> None:
        """Enables minheap creation from exisiting list"""
        self._data = list(array)
        for i in range(len(array) // 2 - 1, -1, -1):
            self._sift_down(i)

    def __bool__(self) -> bool:
        """Allows python to understand list state as True/False"""
        return bool(self._data)

    def __len__(self) -> int:
        """Allows len() to be used on heap"""
        return len(self._data)

    def __repr__(self) -> str:
        """Defines how print(heap) will display data"""
        return f"HeapQueue({self._data})"


class Utils:
    """Utils class, groups static methods."""
    @staticmethod
    def init_drones(graph: Graph) -> list[Drone]:
        """
        Initializes nb_drones drones for the simulation.

        Parameters:
        graph(Graph): graph object which contains all information.

        Returns:
        list[Drone]: list of every drone which will be in the simulation.
        """
        assert graph.start is not None, "Graph has no start node"
        assert graph.end is not None, "Graph has no end node"
        return [Drone(id=f"D{i}",
                      origin=graph.start.name,
                      destination=graph.end.name,
                      priority=i,
                      path=[])
                for i in range(graph.nb_drones)]

    @staticmethod
    def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font,
                  color: tuple[int, int, int], x: int, y: int) -> None:
        """
        Method to draw text to screen with custom params.

        Parameters:
        screen(pygame.Surface): surface in which to draw
        text(str): the text to draw
        font(pygame.font.Font): font in which to draw
        color(tuple[int, int, int]): rgb tuple containing the color of the text
        x(int): desired x in which to position text in screen
        y(int): desired y in which to position text in screen
        """
        image = font.render(text, True, color)
        screen.blit(image, (x, y))

    @staticmethod
    def draw_text_box(screen: pygame.Surface, text: str,
                      text_color: tuple[int, int, int],
                      font: pygame.font.Font, bg_color: tuple[int, int, int],
                      x: int, y: int, padding: int) -> None:
        """
        Method to draw text to screen with custom background.

        Parameters:
        screen(pygame.Surface): surface in which to draw
        text_color(tuple[int, int, int]): rgb tuple defining the color of
        the text
        font(pygame.font.Font): font in which to draw
        bg_color(tuple[int, int, int]): rgb tuple defining background color
        x(int): desired x in which to position text box in screen
        y(int): desired y in which to position text box in screen
        """
        image = font.render(text, True, text_color)
        text_box = image.get_rect(topleft=(x, y))
        bg_rect = pygame.Rect(text_box.x - padding, text_box.y - padding,
                              text_box.width + padding*2,
                              text_box.height + padding*2)
        pygame.draw.rect(screen, bg_color, bg_rect, 0)
        screen.blit(image, (x, y))

    @staticmethod
    def drone_offset(index: int, total_drones: int) -> tuple[float, float]:
        """Method which offsets drone positioning within nodes so that they
        are all visible.

        Parameters:
        index(int): index of current drone relative to the others
        total_drones(int): total number of drones

        Returns:
        tuple[float, float]: new starting coordinates with right offset
        """
        radius = 5
        if total_drones <= 1:
            return 0.0, 0.0
        angle = 2 * pi * index / total_drones
        return radius * cos(angle), radius * sin(angle)
