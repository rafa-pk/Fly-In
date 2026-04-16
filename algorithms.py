import pygame as pygame
from graph_classes import Graph, Node, Edge
from algo_classes import Node, Utils, HeapQueue


# class ReservationTable:


class FleetPlanner:

    def __init__(self, drones: Drone, graph: Graph) -> None:
        self.drones = drones
        self.graph = graph

    def space_time_astar(drone: Drone) -> list[tuple[str, float]]:
        pass


    def register_path(drone: Drone, path: Path) -> None:
        pass

    def plan_routes(self) -> None:
        for drone in sorted(self.drones, key=lambda field: drone.priority):
            path = self.space_time_astar(drone)
            if path:
                drone.path = path
                drone.status = "routing"
                self._register_path(drone, path)
            else:
                drone.status = "failed"
