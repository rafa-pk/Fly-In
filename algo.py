from graph_classes import Graph, ZoneTypes
from algo_classes import Drone, HeapQueue


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
        self._edge_count[(src, dest, t)] = self._edge_count.get((src, dest, t),
                                                                0) + 1

    def drone_count_at_t(self, node: str, t: int) -> int:
        return self._zone_count.get((node, t), 0)

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
                dest, next_t = path[i + 1]
                self._reserve_edge(node, dest, next_t)
                for intermediate_t in range(t + 1, next_t):
                    self._reserve_node(dest, intermediate_t)


class FleetPlanner:

    def __init__(self, drones: list[Drone], graph: Graph) -> None:
        self.drones = drones
        self.graph = graph
        self.res_table = ReservationTable()

    def reconstruct_path(self, previous: dict[tuple[str, int],
                                              tuple[str, int]],
                         t: int) -> list[tuple[str, int]]:
        path: list[tuple[str, int]] = []
        current_state: tuple[str, int] = (self.graph.end.name, t)

        while current_state in previous:
            path.append(current_state)
            current_state = previous[current_state]
        path.append(current_state)
        path.reverse()
        return path

    def rev_dijkstra(self, curr_hub: str, t: int) -> dict[str, int]:
        stack = HeapQueue()
        visited = set()
        cost_log: dict[tuple[str, int], int] = {}

        stack.push((0, self.graph.end.name))
        while stack:
            cost, node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            cost_log[node] = cost
            if node == curr_hub:
                return cost_log
            for connection in self.graph.connections[node]:
                node1, node2 = connection.connection
                neighbour = node2 if node1 == node else node1
                if self.graph.nodes[neighbour].zone == ZoneTypes.BLOCKED:
                    continue
                neighbour_cost = (cost + connection.cost +
                                  self.res_table.drone_count_at_t(neighbour,
                                                                  t))
                if (neighbour not in cost_log or
                        neighbour_cost < cost_log[neighbour]):
                    cost_log[neighbour] = neighbour_cost
                    stack.push((neighbour_cost, neighbour))
        return {}

    def sta_star(self) -> list[tuple[str, int]]:
        possibilities = HeapQueue()
        heuristic: dict[str, int] = {}
        visited = set()
        cost_log: dict[[str, int], int] = {}
        previous: dict[tuple[str, int], tuple[str, int]] = {}

        possibilities.push((0, self.graph.start.name, 0))
        while possibilities:
            cost, node, t = possibilities.pop()
            if (node, t) in visited:
                continue
            visited.add((node, t))
            cost_log[(node, t)] = cost
            heuristic = self.rev_dijkstra(node, t)
            if node == self.graph.end.name:
                return self.reconstruct_path(previous, t)
            for connection in self.graph.connections[node]:
                node1, node2 = connection.connection
                neighbour = node2 if node1 == node else node1
                if (self.graph.nodes[neighbour].zone == ZoneTypes.BLOCKED or
                        neighbour not in heuristic):
                    continue
                neighbour_cost = cost + connection.cost + heuristic[neighbour]
                if self.graph.nodes[neighbour].zone == ZoneTypes.PRIORITY:
                    neighbour_cost -= 1
                neighbour_t = t + connection.cost
                neighbour_max_drones = self.graph.nodes[neighbour].max_drones
                mlc = connection.max_link_capacity
                if (self.res_table.zone_is_full(neighbour, neighbour_t,
                                                neighbour_max_drones) or
                        any(self.res_table.edge_is_full(node, neighbour,
                                                        neighbour_t,
                                                        mlc)
                            for intermediate in range(connection.cost))):
                    continue
                going_to_neighbour = (neighbour, neighbour_t)
                if (going_to_neighbour not in cost_log or
                        neighbour_cost < cost_log[going_to_neighbour]):
                    cost_log[going_to_neighbour] = neighbour_cost
                    previous[going_to_neighbour] = (node, t)
                    possibilities.push((neighbour_cost, neighbour,
                                        neighbour_t))
            waiting_cost = cost + 1 + heuristic[node]
            waiting_t = t + 1
            waiting = (node, waiting_t)
            max_drones = self.graph.nodes[node].max_drones
            if not self.res_table.zone_is_full(node, waiting_t, max_drones):
                if waiting not in cost_log or waiting_cost < cost_log[waiting]:
                    cost_log[waiting] = waiting_cost
                    previous[waiting] = (node, t)
                    possibilities.push((waiting_cost, node, waiting_t))
        return []

    def plan_routes(self) -> None:
        for drone in sorted(self.drones, key=lambda drone: drone.priority):
            drone.path = self.sta_star()
            drone.status = "routing"
            self.res_table.reserve_path(drone.path)
