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


class Utils:

    @staticmethod
    def init_drones(graph: Graph) -> list[Drone]:
        return [Drone(id=f"drone_{i}",
                      origin=graph.start.name,
                      destination=graph.end.name,
                      priority=i,
                      path=[])
                for i in range(graph.nb_drones)]