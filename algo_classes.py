from typing import Any
from dataclasses import dataclass 
from graph_classes import Graph


@dataclass
class Drone:
    id: str
    origin: str
    destination: str
    priority: int
    path: list[tuple[str, float]]
    status: str = "idle"

    # def reconstruct_path(self, path, node, t)


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
        return bool(self.data) 

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"HeapQueue({self._data})"


class Utils:

    @staticmethod
    def init_drones(graph: Graph) -> list[Drone]:
        return [Drone(id=f"drone_{i}",
                      origin=graph.start.name,
                      destination=graph.end.name,
                      priority=i,
                      path=[])
                for i in range(graph.nb_drones)]
