import sys
from enum import Enum
from pygame import Color
from typing import Self
from pydantic import BaseModel, Field, model_validator


class MapEntries(Enum):
    """Enum defining valid map entries"""
    NB_DRONES = "nb_drones"
    START_HUB = "start_hub"
    HUB = "hub"
    END_HUB = "end_hub"
    CONNECTION = "connection"


class MetadataKeys(Enum):
    """Enum defining valid metadata"""
    COLOR = "color"
    ZONE = "zone"
    MAX_DRONES = "max_drones"
    MAX_LINK_CAPACITY = "max_link_capacity"


class NodeTypes(Enum):
    """Enum defining valid Nodes"""
    HUB = "hub"
    START = "start_hub"
    END = "end_hub"


class ZoneTypes(Enum):
    """Enum defining valid ZoneTypes"""
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Node(BaseModel):
    """Node BaseModel class, defines and validates its attrs."""
    name: str = Field(min_length=1)
    type: NodeTypes
    x: int
    y: int
    zone: ZoneTypes = Field(default=ZoneTypes.NORMAL)
    color: str = Field(default="green")
    max_drones: int = Field(default=1, ge=1)

    @model_validator(mode='after')
    def node_validator(self) -> Self:
        """model_validator to validate node_data after object creation."""
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


class Edge(BaseModel):
    """Edge BaseModel class, defines and validates its attrs"""
    connection: tuple[str, str]
    cost: int
    max_link_capacity: int = Field(default=1, ge=1)
    color: str = "black"


class Graph:
    """Class representing node graph."""
    def __init__(self) -> None:
        """Initialization method for Graph class"""
        self.nb_drones: int = 0
        self.nodes: dict[str, Node] = {}
        self.start: Node | None = None
        self.end: Node | None = None
        self.connections: dict[str, list[Edge]] = {}

    def add_node(self, node: Node) -> None:
        """Method which allows to add valid node to node list in graph."""
        if node.name in self.nodes:
            raise ValueError(f"Name '{node.name}' already exists")
        self.nodes[node.name] = node
        self.connections[node.name] = []
        if node.type == NodeTypes.START:
            self.start = node
        elif node.type == NodeTypes.END:
            self.end = node

    def add_edge(self, edge: Edge) -> None:
        """Method which allows to add valid edge to edge list in graph."""
        node1, node2 = edge.connection
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Connection between nodes unsuccessful (node name"
                             " is unkown or unvalid)")
        if node1 == node2:
            raise ValueError("Connection between nodes unsuccessful (connected"
                             " nodes cannot have the same name)")
        self.connections[node1].append(edge)
        self.connections[node2].append(edge)

    def validate(self) -> None:
        """Last parsing layer, validates remaining information/raises errors"""
        seen = set()

        if self.nb_drones < 0:
            raise ValueError("'nb_drones' value cannot be negative")
        if self.start is None:
            raise ValueError("Graph has no 'start_hub'")
        if self.end is None:
            raise ValueError("Graph has no 'end_hub'")
        coordinates = [(node.x, node.y) for node in self.nodes.values()]
        if len(coordinates) != len(set(coordinates)):
            raise ValueError("Graph has duplicate coordinates")
        for node, edges in self.connections.items():
            for edge in edges:
                node1, node2 = edge.connection
                neighbour = node2 if node1 == node else node1
                if node > neighbour:
                    continue
                pair = frozenset({node, neighbour})
                if pair in seen:
                    raise ValueError(f"Duplicate connection: '{node}' and "
                                     f"'{neighbour}' were already connected")
                seen.add(pair)
