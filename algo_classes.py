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


class HeapQueue:

    def __init__(self) -> None:
        self.data = []

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self.data[parent] <= self.data[i]:
                break
           self.data[parent], self.data[i] = self.data[i], self.data[parent]
           i = parent 

    def _sift_down(self, i: int) -> None:
        len = len(self.data)
        while True:
            smallest = i
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            if left_child < len and self.data[left] < self.data[smallest]

    def push(self, value: int) -> None:
        list.append(value)
        self._sift_up(len(self.data) - 1)

    def pop(self, value: int) -> int:
        if not self.data:
            raise ValueError("Attempt to pop from empty heap")
        self.data[0], self.data[-1] = self.data[-1], self.data[0]
        min = self.data.pop()
        if self.data:
            self._sift_down(0)
        return min


class Utils:

    @staticmethod
    def init_drones(graph: Graph) -> list[Drone]:
        return [Drone(id=f"drone_{i}",
                      origin=graph.start.name,
                      destination=graph.end.name,
                      priority=i,
                      path=[])
                for i in range(graph.nb_drones)]