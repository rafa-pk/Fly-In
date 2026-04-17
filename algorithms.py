import pygame as pygame
from graph_classes import Graph, Node, Edge
from algo_classes import Drone, Utils, HeapQueue


# class ReservationTable:


class FleetPlanner:

    def __init__(self, drones: Drone, graph: Graph) -> None:
        self.drones = drones
        self.graph = graph

    def space_time_astar(drone: Drone) -> list[tuple[str, float]]:
        open_set = HeapQueue()
        g_cost = dict(tuple[str, int], float)
        previous = dict(tuple[str, int], tuple[str, int])
        visited = set()

        open_set.push((0, self.graph.start.name, 0))
        while open_set:
            f, node, t = open_set.pop()
            if node in visited:
                pass
            if node == self.graph.end.name:
                return drone.path
            for edge in self.graph.edges["node"]:
                # compute g cost
                # compute total cost (f)
                # skip if blocked
                # push to heap
                # check reservation table, skip if reserved
                # if better g cost, push to heap and store in previous
            # compute waiting turn
            # if reserved skip
            # if waiting is less costly, push



    def plan_routes(self) -> None:
        for drone in sorted(self.drones, key=lambda field: drone.priority):
            path = self.space_time_astar(drone)
            if path:
                drone.path = path
                drone.status = "routing"
                # reserve it
            else:
                drone.status = "failed"
