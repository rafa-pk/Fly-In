import pygame as pygame
from graph_classes import Graph, Node, Edge, ZoneTypes
from algo_classes import Drone, Utils, HeapQueue


class ReservationTable:

    def __init__(self) -> None:
        self._table = set()
        # implement zone limitations and edge limitations

    def _reserve(self, node: str, t: int) -> None:
        self._table.add((node, t))

    def is_reserved(self, node: str, t: int) -> bool:
        if (node, t) in self._table:
            return True
        return False

    def reserve_path(self, path: list[tuple[str, int]]) -> None:
        for node, t in path:
            self._reserve(node, t)


class FleetPlanner:

    def __init__(self, drones: list[Drone], graph: Graph) -> None:
        self.drones = drones
        self.graph = graph
        self.reservation_table = ReservationTable()

    def reconstruct_path(self, previous: dict[tuple[str, int], int], t: int) -> list[tuple[str, int]]:
        path: list[tuple[str, int]] = []
        current_state: tuple[str, int] = (self.graph.end.name, t)

        while current_state in previous:
            path.append(current_state)
            current_state = previous[current_state]
        path.append(current_state)
        path.reverse()
        return path

    def space_time_astar(self) -> list[tuple[str, float]]:
        open_set = HeapQueue()
        g_cost: dict[tuple[str, int], float] = {}
        previous: dict[tuple[str, int], tuple[str, int]] = {}
        visited = set()

        open_set.push((0, self.graph.start.name, 0))
        while open_set:
            g, node, t = open_set.pop()
            if (node, t) in visited:
                continue
            visited.add((node, t))
            if node == self.graph.end.name:
                return self.reconstruct_path(previous, t)
            for edge in self.graph.connections[node]:
                neighbour = edge.connection[1]
                new_g_cost = g + edge.cost
                if (self.graph.nodes[neighbour].zone == ZoneTypes.RESTRICTED or
                        self.reservation_table.is_reserved(neighbour, t + 1)):  # take into account zone limitations / edge limitations
                    continue
                new_option = (neighbour, t + 1)
                if new_option not in g_cost or new_g_cost < g_cost[new_option]:
                    g_cost[new_option] = new_g_cost
                    previous[new_option] = (node, t)
                    open_set.push((new_g_cost, neighbour, t + 1))
            waiting_option = (node, t + 1)
            if not self.reservation_table.is_reserved(node, t + 1):
                new_g_cost = g + 1
                if waiting_option not in g_cost or new_g_cost < g_cost[waiting_option]:
                    g_cost[waiting_option] = new_g_cost
                    previous[waiting_option] = (node, t)
                    open_set.push((new_g_cost, node, t + 1))
        return self.reconstruct_path(previous, t)

    def plan_routes(self) -> None:
        for drone in sorted(self.drones, key=lambda drone: drone.priority):
            path = self.space_time_astar()
            print(path)
            if path:
                drone.path = path
                drone.status = "routing"
                self.reservation_table.reserve_path(path)
            else:
                drone.status = "failed"
