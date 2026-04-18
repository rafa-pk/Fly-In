import sys
from enum import Enum
from pygame import Color
from typing import Any, Self
from pydantic import BaseModel, ValidationError, Field, model_validator


class MapEntries(Enum):
    NB_DRONES = "nb_drones"
    START_HUB = "start_hub"
    HUB = "hub"
    END_HUB = "end_hub"
    CONNECTION = "connection"


class MetadataKeys(Enum):
    COLOR = "color"
    ZONE = "zone"
    MAX_DRONES = "max_drones"
    MAX_LINK_CAPACITY = "max_link_capacity"


class NodeTypes(Enum):
    HUB = "hub"
    START = "start_hub"
    END = "end_hub"


class ZoneTypes(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Node(BaseModel):
    name: str = Field(min_length=1)
    type: NodeTypes
    x: int  # = Field(ge=0)
    y: int  # = Field(ge=0)
    zone: ZoneTypes = Field(default=ZoneTypes.NORMAL)
    color: str = Field(default="green")
    max_drones: int = Field(default=None, ge=1)

    @model_validator(mode='after')
    def node_validator(self) -> Self:
        if '-' in self.name:
            raise ValueError("Parsing Error: Zone names cannot contain dashes")
            sys.exit(1)
        try:
            Color(self.color)
        except ValueError:
            raise ValueError(f"Parsing Error: Map format not supported: "
                             f"{self.color} is not a valid color")
            sys.exit(1)
        return self

    def euclidean_distance_to(self, node: Self) -> float:
        return round((((self.x - node.x) ** 2 + (self.y - node.y) ** 2) ** 0.5), 2)


class Edge(BaseModel):
    connection: tuple[str, str]
    cost: int
    max_link_capacity: int = Field(default=1, ge=1)
    color: str = "black"


class Graph:
    
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.nodes: dict[str, Node] = {}
        self.start: Node | None = None
        self.end: Node | None = None
        self.connections: dict[str, list[Edge]] = {}

    def add_node(self, node: Node) -> None:
        if node.name in self.nodes:
            raise ValueError(f"Name '{node.name}' already exists")
        self.nodes[node.name] = node
        self.connections[node.name] = []
        if node.type == NodeTypes.START:
            self.start = node
        elif node.type == NodeTypes.END:
            self.end = node

    def add_edge(self, edge: Edge) -> None:
        node1, node2 = edge.connection
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError(f"Connection between nodes unsuccessful (node name is unkown or unvalid)")
        if node1 == node2:
            raise ValueError(f"Connection between nodes unsuccessful (connected nodes cannot have the same name)")
        self.connections[node1].append(edge)
        self.connections[node2].append(edge)

    def validate(self) -> None:
        seen = set()

        if self.start is None:
            raise ValueError("Graph has no 'start_hub'")
        if self.end is None:
            raise ValueError("Graph has no 'end_hub'")
        coordinates = [(node.x, node.y) for node in self.nodes.values()]
        if len(coordinates) != len(set(coordinates)):
            raise ValueError("Graph has duplicate coordinates")
        for node, edges in self.connections.items():
            for edge in edges:
                pair = frozenset({node, edge.connection[1]})
                if pair in seen:
                    raise ValueError(f"Duplicate connection: '{node}' and '{edge.connection[1]}' were already connected")
                seen.add(pair)
