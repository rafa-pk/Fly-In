import pygame as pygame
from graph_classes import Graph, Node, Edge, ZoneTypes
from algo_classes import Drone, Utils, HeapQueue


class ReservationTable:

    def __init__(self) -> None:
        self._table = set()
        self._zone_count: dict[tuple[str, int], int] = {}
        self._edge_count: dict[tuple[str, int], int] = {}

    def _reserve(self, node: str, t: int) -> None:
        self._table.add((node, t))

    def _reserve_node(self, node: str, t: int) -> None:
        self._zone_count[(node, t)] = self._zone_count.get((node, t), 0) + 1

    def _reserve_edge(self, src: str, dest: str, t: int) -> None:
        self._edge_count[(src, dest, t)] = self._edge_count.get((src, dest, t), 1) + 1

    def is_reserved(self, node: str, t: int) -> bool:
        if (node, t) in self._table:
            return True
        return False

    def zone_is_full(self, node: str, t: int, max_drones: int) -> bool:
        if max_drones is None:
            return False
        if self._zone_count.get((node, t), 0) >= max_drones:
            return True
        return False

    def edge_is_full(self, src: str, dest: str, t: int, max_link: int) -> bool:
        if self._edge_count.get((src, dest, t), 0) >= max_link:
            return True
        return False

    def reserve_path(self, path: list[tuple[str, int]]) -> None:
        for i, (node, t) in enumerate(path):
            self._reserve(node, t)
            self._reserve_node(node, t)
            if i < len(path) - 1:
                dest, _ = path[i + 1]
                self._reserve_edge(node, dest, t)


class FleetPlanner:

    def __init__(self, drones: list[Drone], graph: Graph) -> None:
        self.drones = drones
        self.graph = graph
        self.res_table = ReservationTable()

    def reconstruct_path(self, previous: dict[tuple[str, int], int], t: int) -> list[tuple[str, int]]:
        path: list[tuple[str, int]] = []
        current_state: tuple[str, int] = (self.graph.end.name, t)

        while current_state in previous:
            path.append(current_state)
            current_state = previous[current_state]
        path.append(current_state)
        path.reverse()
        return path

    def sta_star(self) -> list[tuple[str, int]]:
        possibilities = HeapQueue()
        g_cost_log: dict[tuple[str, int], float] = {}
        previous: dict[tuple[str, int], tuple[str, int]] = {}
        visited = set()

        possibilities.push((0, self.graph.start.name, 0))
        while possibilities:
            g_cost, node, t = possibilities.pop()
            # print(f"pop ({node}, t={t}) g={g_cost}")
            if (node, t) in visited:
                continue
            visited.add((node, t))
            if node == self.graph.end.name:
                # print("Gros caca qui pue")
                return self.reconstruct_path(previous, t)
            for edge in self.graph.connections[node]:
                node1, node2 = edge.connection
                neighbour = node2 if node1 == node else node1
                time_t = t + edge.cost
                if self.graph.nodes[neighbour].zone == ZoneTypes.PRIORITY:
                    g_cost_to_neighbour = g_cost + edge.cost - 0.1
                else:
                    g_cost_to_neighbour = g_cost + edge.cost
                neighbour_max_drones = self.graph.nodes[neighbour].max_drones
                if (self.graph.nodes[neighbour].zone == ZoneTypes.BLOCKED or
                        self.res_table.is_reserved(neighbour, time_t) or
                        self.res_table.zone_is_full(neighbour, time_t, neighbour_max_drones) or
                        self.res_table.edge_is_full(node, neighbour, time_t, edge.max_link_capacity)): 
                    continue
                move_possibility = (neighbour, time_t)
                if (move_possibility not in g_cost_log or
                        g_cost_to_neighbour < g_cost_log[move_possibility]):
                    g_cost_log[move_possibility] = g_cost_to_neighbour
                    previous[move_possibility] = (node, t)
                    possibilities.push((g_cost_to_neighbour, neighbour, time_t))
            wait_possibility = (node, t + 1)
            max_drones = self.graph.nodes[node].max_drones
            if (not self.res_table.is_reserved(node, t + 1) 
                    and not self.res_table.zone_is_full(node, t + 1, max_drones)): 
                wait_g_cost = g_cost + 1
                if wait_possibility not in g_cost_log or wait_g_cost < g_cost_log[wait_possibility]:
                    g_cost_log[wait_possibility] = wait_g_cost
                    previous[wait_possibility] = (node, t)
                    possibilities.push((wait_g_cost, node, t + 1))
        return []

    def plan_routes(self) -> None:
        for drone in sorted(self.drones, key=lambda drone: drone.priority):
            path = self.sta_star()
            if path:
                drone.path = path
                drone.status = "routing"
                self.res_table.reserve_path(path)
            else:
                drone.status = "failed"
